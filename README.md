# ASAP API

## Docker

### Build

### Run

```shell
docker run -it -w /local -v $PWD:/local -v /data/asap:/data/asap -p 8000:8000 --entrypoint sh asap-api:0.1

/local/src # fastapi run main.py 
```

## API

### Configuration

Configuration variables are retrieved in this order :

* Environment Variable
* Configuration file
* Default value

| Environment variable | Config file variable | Default               | Description              |
|----------------------|----------------------|-----------------------|--------------------------|
| `ASAP_CONFIG_FILE`   | N/A                  | `config.json`         | Configuration file       |
|||||
| `ASAP_DATA_DIR`      | `data_dir`           | `data`                | ASAP Data Root directory |
| `ASAP_DATA_CVE_DIR`  | `data_cve_dir`       | `{ASAP_DATA_DIR}/cve` | ASAP CVE Data directory  |
| `ASAP_DATA_CWE_DIR`  | `data_cwe_dir`       | `{ASAP_DATA_DIR}/cwe` | ASAP CWE Data directory  |
