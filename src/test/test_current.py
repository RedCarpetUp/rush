import contextlib
from io import StringIO

import alembic
import sqlalchemy
from alembic.command import current as alembic_current
from hypothesis import given
from hypothesis.strategies import (
    integers,
    text,
)

from rush.exceptions import *
from rush.models import (
    User,
    UserPy,
)


def test_current(getAlembic: alembic.config.Config) -> None:
    """Test that the alembic current command does not erorr"""
    # Runs with no error
    # output = run_alembic_command(pg["engine"], "current", {})

    stdout = StringIO()
    with contextlib.redirect_stdout(stdout):
        # command_func(alembic_cfg, **command_kwargs)
        alembic_current(getAlembic, {})
    assert stdout.getvalue() == ""
    # assert output == ""


def test_user2(session: sqlalchemy.orm.session.Session) -> None:
    u = User(
        performed_by=123,
        id=101,
        name="dfd",
        fullname="dfdf",
        nickname="dfdd",
        email="asas",
    )
    session.add(u)
    session.commit()
    a = session.query(User).first()
    print(a.id)
    u = UserPy(
        id=a.id,
        performed_by=123,
        email="sss",
        name="dfd",
        fullname="dfdf",
        nickname="dfdd",
    )


def test_user(session: sqlalchemy.orm.session.Session) -> None:
    u = User(
        performed_by=123,
        id=102,
        name="dfd",
        fullname="dfdf",
        nickname="dfdd",
        email="asas",
    )
    session.add(u)
    session.commit()
    a = session.query(User).first()
    u = UserPy(
        performed_by=123,
        email="sss",
        id=a.id,
        name="dfd",
        fullname="dfdf",
        nickname="dfdd",
    )


# if you remove min_value=2, you will see the errors
@given(integers(min_value=103, max_value=999999))
def test_user3(session: sqlalchemy.orm.session.Session, id: int) -> None:
    u = User(
        performed_by=123,
        id=id,
        name="dfd",
        fullname="dfdf",
        nickname="dfdd",
        email="asas",
    )
    session.add(u)
    session.commit()
    a = session.query(User).first()
    u = UserPy(
        performed_by=123,
        email="sss",
        id=a.id,
        name="dfd",
        fullname="dfdf",
        nickname="dfdd",
    )
