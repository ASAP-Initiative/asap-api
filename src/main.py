from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from aiokafka import AIOKafkaConsumer
import asyncio
import json
import os
import asyncpg
from typing import Optional

app = FastAPI()

ASAP_DB_HOST = os.getenv("ASAP_DB_HOST", "asap-db")
ASAP_DB_PORT = os.getenv("ASAP_DB_PORT", "5432")
ASAP_DB_NAME = os.getenv("ASAP_DB_NAME", "asap")
ASAP_DB_USER = os.getenv("ASAP_DB_USER", "asap")
ASAP_DB_PASSWORD = os.getenv("ASAP_DB_PASSWORD", "asap_pass")

DB_URL = f"postgres://{ASAP_DB_USER}:{ASAP_DB_PASSWORD}@{ASAP_DB_HOST}:{ASAP_DB_PORT}/{ASAP_DB_NAME}"

print(f"{DB_URL}")

ASAP_KAFKA_BROKERS = os.getenv("ASAP_KAFKA_BROKERS", "kafka-broker:9092")
ASAP_KAFKA_TOPIC = os.getenv("ASAP_KAFKA_TOPIC", "asap")

#GROUP_ID = os.getenv("KAFKA_GROUP_ID", "asap-api-group")


async def consume_loop(consumer: AIOKafkaConsumer, pool: asyncpg.pool.Pool):
    await consumer.start()
    try:
        async for msg in consumer:
            # Decode value
            try:
                raw = msg.value.decode("utf-8")
            except Exception:
                raw = msg.value.hex()

            # Try parse JSON, otherwise treat as raw string
            parsed = None
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = None

            # Extract only data.host, data.task, data.status, data.result
            host = None
            task = None
            status = None
            result = None

            if isinstance(parsed, dict):
                data = parsed.get("data") if "data" in parsed else parsed.get("payload") or parsed.get("body") or None
                if isinstance(data, dict):
                    host = data.get("host")
                    task = data.get("task")
                    status = data.get("status")
                    result = data.get("result")
                else:
                    # no structured data; fallback: keep entire parsed as result
                    result = parsed
            else:
                # not JSON: store raw string in result
                result = raw

            key_str: Optional[str]
            try:
                key_str = msg.key.decode("utf-8") if msg.key else None
            except Exception:
                key_str = None

            # Insert into DB (store only extracted fields; result as jsonb when possible)
            try:
                result_json = None
                if result is not None:
                    # if result is already a dict/list -> dump to json string; else keep as string
                    if isinstance(result, (dict, list)):
                        result_json = json.dumps(result)
                    else:
                        # try parse if it's a JSON string
                        try:
                            json.loads(result)  # type: ignore
                            result_json = result  # it's valid json string
                        except Exception:
                            # store as JSON string value
                            result_json = json.dumps({"raw": str(result)})
                await pool.execute(
                    """
                    INSERT INTO messages(host, task, status, result)
                    VALUES($1, $2, $3, $4)
                    """,
                    host,
                    task,
                    status,
                    result_json,
                )
                print(f"Inserted message task={task}")
            except Exception as e:
                # log minimal error; avoid crashing the consumer loop
                print(f"DB insert failed: {e}")
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event():
    # Init DB pool
    pool = await asyncpg.create_pool(DB_URL)
    app.state.db = pool

    # Ensure table exists
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id bigserial PRIMARY KEY,
                host text,
                task text,
                status text,
                result jsonb,
                received_at timestamptz DEFAULT now()
            );
            """
        )

    # Init Kafka consumer and start background consume task
    consumer = AIOKafkaConsumer(
        ASAP_KAFKA_TOPIC,
        bootstrap_servers=ASAP_KAFKA_BROKERS,
        #group_id=GROUP_ID,
        enable_auto_commit=True,
    )
    app.state.consumer = consumer
    #app.state.consumer_task = asyncio.create_task(consume_loop(consumer, pool))

@app.on_event("startup")
@repeat_every(seconds=5)
def kafka_consume():
    asyncio.create_task(consume_loop(app.state.consumer, app.state.db))

@app.on_event("shutdown")
async def shutdown_event():
    # Cancel consumer task
    task = getattr(app.state, "consumer_task", None)
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    # Close DB pool
    pool = getattr(app.state, "db", None)
    if pool:
        await pool.close()


@app.get("/")
async def read_root():
    return {"message": "Kafka Consumer is running and saving messages to DB."}


@app.get("/messages/count")
async def messages_count():
    pool = getattr(app.state, "db", None)
    if not pool:
        return {"count": 0}
    async with pool.acquire() as conn:
        row = await conn.fetchval("SELECT count(1) FROM messages;")
        return {"count": row}

@app.get("/hosts/{host}/tasks")
async def list_tasks_for_host(host: str, limit: int = 100, offset: int = 0):
    """
    Return tasks for a given host. Pagination via limit/offset.
    """
    pool = getattr(app.state, "db", None)
    if not pool:
        raise HTTPException(status_code=503, detail="database not initialized")

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, task, status, result, received_at
            FROM messages
            WHERE host = $1
            ORDER BY received_at DESC
            LIMIT $2 OFFSET $3
            """,
            host,
            limit,
            offset,
        )

    def _serialize_row(r):
        return {
            "id": r["id"],
            "task": r["task"],
            "status": r["status"],
            "result": r["result"],
            "received_at": r["received_at"].isoformat() if r["received_at"] else None,
        }

    return [_serialize_row(r) for r in rows]