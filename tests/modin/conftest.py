"""Registers fixtures for core"""

import os

import pytest

# pylint: disable=unused-import
from tests.core.checks_fixtures import custom_check_teardown  # noqa

ENGINES = os.getenv("CI_MODIN_ENGINES", "").split(",")
if ENGINES == [""]:
    ENGINES = ["ray", "dask"]


@pytest.fixture(scope="session", params=ENGINES, autouse=True)
def setup_modin_engine(request):
    """Set up the modin engine.

    Eventually this will also support dask execution backend.
    """
    engine = request.param
    os.environ["MODIN_ENGINE"] = engine
    os.environ["MODIN_MEMORY"] = "100000000"
    os.environ["RAY_IGNORE_UNHANDLED_ERRORS"] = "1"

    if engine == "ray":
        # pylint: disable=import-outside-toplevel
        import ray

        ray.init()
        yield
        ray.shutdown()

    elif engine == "dask":
        # pylint: disable=import-outside-toplevel
        from distributed import Client

        client = Client()
        yield
        client.shutdown()
    else:
        raise ValueError(f"Not supported engine: {engine}")
