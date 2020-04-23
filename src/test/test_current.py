import alembic
from app_utils.exceptions import *

import contextlib
from io import StringIO

def test_current(pg) -> None:
    """Test that the alembic current command does not erorr"""
    # Runs with no error
    # output = run_alembic_command(pg["engine"], "current", {})

    stdout = StringIO()
    with contextlib.redirect_stdout(stdout):
            # command_func(alembic_cfg, **command_kwargs)
            alembic.command.current(pg["alembic_cfg"], {})
    assert stdout.getvalue() == ""
    # assert output == ""
