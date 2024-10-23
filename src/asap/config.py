import json
import os
from pydantic import BaseModel

ASAP_CONFIG_FILE = os.getenv('ASAP_CONFIG_FILE', 'config.json')

ASAP_DATA_DIR = os.getenv('ASAP_DATA_DIR', 'data')
ASAP_DATA_CVE_DIR = os.getenv('ASAP_DATA_CVE_DIR', f"{ASAP_DATA_DIR}/cve")
ASAP_DATA_CWE_DIR = os.getenv('ASAP_DATA_CWE_DIR', f"{ASAP_DATA_DIR}/cwe")


class ASAP_Config(BaseModel):
    data_dir: str
    data_cve_dir: str
    data_cwe_dir: str


def _load_config() -> ASAP_Config:
    print(f"Loading ASAP configuration from '{ASAP_CONFIG_FILE}'")
    with open(ASAP_CONFIG_FILE) as conf_fh:
        conf = json.load(conf_fh)
        return ASAP_Config(
            data_dir=os.getenv('ASAP_DATA_DIR', conf['data_dir'] if 'data_dir' in conf else 'data'),
            data_cve_dir=os.getenv('ASAP_DATA_CVE_DIR', conf['data_cve_dir'] if 'data_cve_dir' in conf else f"{ASAP_DATA_DIR}/cve"),
            data_cwe_dir=os.getenv('ASAP_DATA_CWE_DIR', conf['data_cwe_dir'] if 'data_cwe_dir' in conf else f"{ASAP_DATA_DIR}/cwe")
            )

asap_config = _load_config()
