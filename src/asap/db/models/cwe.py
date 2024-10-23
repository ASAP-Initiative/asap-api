from pathlib import Path

import csv
import urllib.request
import zipfile

from asap.db.engine import db_engine
from asap.config import asap_config

from typing import Optional

from sqlmodel import Field, Session, SQLModel, select

class CWE(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    description: str

_cwe_download_url = 'https://cwe.mitre.org/data/csv/1194.csv.zip'

_cwe_data_dir = asap_config.data_cwe_dir
_cwe_csv_file = f"{asap_config.data_cwe_dir}/cwe.csv"
_cwe_zip_file = f"{_cwe_csv_file}.zip"

def download_cwe():
    cwe_data_dir = Path(_cwe_data_dir)
    csv_file = Path(_cwe_csv_file)
    zip_file = Path(_cwe_zip_file)
    if not cwe_data_dir.is_dir():
        print(f"Creating CWE directory '{_cwe_data_dir}...")
        cwe_data_dir.mkdir()
    if not zip_file.exists():
        print(f"Downloading CWE file {_cwe_download_url} into {_cwe_zip_file}...")
        urllib.request.urlretrieve(_cwe_download_url, _cwe_zip_file)
    if not csv_file.exists():
        with zipfile.ZipFile(_cwe_zip_file, 'r') as zip_ref:
            with open(_cwe_csv_file, 'wb') as f:
                print(f"Unzipping CWE zip file {_cwe_zip_file} into {_cwe_csv_file}...")
                f.write(zip_ref.read('1194.csv'))


def cwe_load_data():
    with open(_cwe_csv_file, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        with Session(db_engine) as db_session:
            db_session.
            for row in reader:
                db_session.add(
                    CWE(id=row['CWE-ID'], name=row['Name'], description=row['Description'])
                )
            db_session.commit()


def cwe_by_id(id: str):
    with Session(db_engine) as db_session:
        statement = select(CWE).where(CWE.id == id)
        results = db_session.exec(statement)
        return results.first()


def cwe_list():
    with Session(db_engine) as db_session:
        statement = select(CWE)
        results = db_session.exec(statement)
        return results.all()


# download_cwe()
# cwe_load_data()
