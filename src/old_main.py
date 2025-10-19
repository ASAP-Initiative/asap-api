from fastapi import FastAPI

from asap.api import VERSION
from asap.db.engine import create_db_tables, db_engine
from asap.routers import ansible_collection, config, cve, cwe, metrics

app = FastAPI()

# app.include_router(ansible_collection.router)
app.include_router(config.router)
# app.include_router(cve.router)
app.include_router(cwe.router)
# app.include_router(metrics.router)

@app.get("/version")
def get_version():
    return (VERSION)
