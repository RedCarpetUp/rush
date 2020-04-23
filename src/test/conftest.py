# pylint: disable=redefined-outer-name,no-member

import json
import os
import shutil
import subprocess
import sys
import time
import logging
from pathlib import Path

import alembic
import pytest
from parse import parse
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

import os
from pathlib import Path

from app_utils.pg_function import PGFunction

REPO_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent.parent.resolve()
TEST_RESOURCE_ROOT = REPO_ROOT / "src" / "test" / "resources"
TEST_VERSIONS_ROOT = REPO_ROOT / "src" / "test" / "alembic_config" / "versions"

# from app_utils import TEST_VERSIONS_ROOT
# from app_utils.testbase import reset_event_listener_registry

PYTEST_DB = "postgresql://alem_user:password@localhost:5680/alem_db"


def build_alembic_config(engine: Engine) -> AlembicConfig:
    """Populate alembic configuration from metadata and config file."""
    path_to_alembic_ini = REPO_ROOT / "alembic.ini"

    alembic_cfg = AlembicConfig(path_to_alembic_ini)
    # Make double sure alembic references the test database
    alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
    alembic_cfg.set_main_option("script_location", str((Path("src") / "test" / "alembic_config")))
    return alembic_cfg

@pytest.fixture(scope="session")
def pg() -> None:
    """Creates a postgres 12 docker container that can be connected
    to using the PYTEST_DB connection string"""

    container_name = "app_utils_pg"
    image = "postgres:12"

    connection_template = "postgresql://{user}:{pw}@{host}:{port:d}/{db}"
    conn_args = parse(connection_template, PYTEST_DB)

    # Don't attempt to instantiate a container if
    # we're on CI
    if "GITHUB_SHA" in os.environ:
        yield
        return

    try:
        is_running = (
            subprocess.check_output(
                ["docker", "inspect", "-f", "{{.State.Running}}", container_name]
            )
            .decode()
            .strip()
            == "true"
        )
    except subprocess.CalledProcessError:
        # Can't inspect container if it isn't running
        is_running = False

    # if is_running:
    #     yield
    #     return

    subprocess.call(
        [
            "docker",
            "run",
            "--rm",
            "--name",
            container_name,
            "-p",
            f"{conn_args['port']}:5432",
            "-d",
            "-e",
            f"POSTGRES_DB={conn_args['db']}",
            "-e",
            f"POSTGRES_PASSWORD={conn_args['pw']}",
            "-e",
            f"POSTGRES_USER={conn_args['user']}",
            "--health-cmd",
            "pg_isready",
            "--health-interval",
            "3s",
            "--health-timeout",
            "3s",
            "--health-retries",
            "15",
            image,
        ]
    )
    # Wait for postgres to become healthy
    for _ in range(10):
        out = subprocess.check_output(["docker", "inspect", container_name])
        inspect_info = json.loads(out)[0]
        health_status = inspect_info["State"]["Health"]["Status"]
        if health_status == "healthy":
            break
        else:
            time.sleep(1)
    else:
        raise Exception("Could not reach postgres comtainer. Check docker installation")
    
    engine = create_engine(PYTEST_DB, echo=True)
    session_factory = sessionmaker(bind=engine)
    print('\n----- CREATE TEST DB CONNECTION POOL\n')

    alembic_cfg = build_alembic_config(engine)
    with engine.begin() as connection:
        alembic_upgrade(alembic_cfg, 'head')
    _db = {
        'engine': engine,
        'session_factory': session_factory,
        'alembic_cfg': alembic_cfg
    }

    print(_db)
    logging.getLogger().warning("boo ")
    yield _db
    subprocess.call(["docker", "stop", container_name])
    return


@pytest.fixture(scope="session")
def engine(pg: None):
    """sqlalchemy engine fixture"""
    eng = create_engine(PYTEST_DB)
    yield eng
    eng.dispose()


@pytest.fixture(scope="function")
def reset(engine):
    """Fixture to reset between tests"""

    def run_cleaners():
        # reset_event_listener_registry()
        engine.execute("drop schema public cascade; create schema public;")
        # Remove any migrations that were left behind
        # TEST_VERSIONS_ROOT.mkdir(exist_ok=True, parents=True)
        # shutil.rmtree(TEST_VERSIONS_ROOT)
        # TEST_VERSIONS_ROOT.mkdir(exist_ok=True, parents=True)
        # engine.execute(DROP_ALL_FUNCTIONS_SQL)

    run_cleaners()

    yield

    run_cleaners()
