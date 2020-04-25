import alembic
from alembic.command import current as alembic_current
from app_utils.exceptions import *
from app_utils.models import User, UserPy

import contextlib
from io import StringIO

def test_current(alembic) -> None:
    """Test that the alembic current command does not erorr"""
    # Runs with no error
    # output = run_alembic_command(pg["engine"], "current", {})

    stdout = StringIO()
    with contextlib.redirect_stdout(stdout):
            # command_func(alembic_cfg, **command_kwargs)
            alembic_current(alembic, {})
    assert stdout.getvalue() == ""
    # assert output == ""




def test_user2(session) -> None:
        u = User(id=101,performed_by=123, user_id=101,name="dfd",fullname="dfdf",nickname="dfdd",email='asas')
        session.add(u)
        session.commit()
        a = session.query(User).first()
        print(a.id)
        u = UserPy(id=101,performed_by=123,email='sss', user_id=101,name="dfd",fullname="dfdf",nickname="dfdd")

def test_user(session) -> None:
        u = User(id=100,performed_by=123, user_id=101,name="dfd",fullname="dfdf",nickname="dfdd",email='asas')
        session.add(u)
        session.commit()
        a = session.query(User).first()
        print(a.id)
        u = UserPy(id=100,performed_by=123,email='sss', user_id=101,name="dfd",fullname="dfdf",nickname="dfdd")