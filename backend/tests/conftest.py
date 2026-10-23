"""Testlerin ortak hazırlıkları (fixture'lar).

pytest bu dosyayı kendiliğinden bulur ve buradaki fixture'ları bütün test
dosyalarına sunar. Testler geliştirme veritabanına (becomeself) dokunmaz,
ayrı bir test veritabanı (becomeself_test) kullanır.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app import models  # noqa: F401  (tabloları Base.metadata'ya tanıtır)
from app.config import settings
from app.db import Base, get_db
from app.main import app

DEV_DATABASE_URL = make_url(settings.database_url)
TEST_DATABASE_URL = DEV_DATABASE_URL.set(database=f"{DEV_DATABASE_URL.database}_test")


def create_test_database_if_missing() -> None:
    # CREATE DATABASE bir işlem (transaction) içinde çalışamaz, bu yüzden AUTOCOMMIT.
    admin_engine = create_engine(
        DEV_DATABASE_URL.set(database="postgres"), isolation_level="AUTOCOMMIT"
    )
    with admin_engine.connect() as conn:
        exists = conn.scalar(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": TEST_DATABASE_URL.database},
        )
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{TEST_DATABASE_URL.database}"'))
    admin_engine.dispose()


@pytest.fixture(scope="session")
def engine():
    """Bütün test oturumu boyunca bir kez: test veritabanını ve tabloları hazırla."""
    create_test_database_if_missing()
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db(engine):
    """Her test için: bir işlem başlat, test bitince hepsini geri al."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db):
    """Uygulamaya istek atan test istemcisi. get_db yerine test oturumunu kullanır."""
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
