import pytest

from pydantic import ValidationError
from drive_to_es.entities import Env


def test_env_entity(env):
    env = Env()

    assert isinstance(env, Env)


def test_invalid_es_host():
    env_attrs = {
        "es_host": "localhost:9200",
        "service_account_info": '{"key", "value"}'
    }

    with pytest.raises(ValidationError):
        Env(**env_attrs)


def test_invalid_service_account_info():
    env_attrs = {
        "es_host": "http://localhost:9200",
        "service_account_info": "hoge"
    }

    with pytest.raises(ValidationError):
        Env(**env_attrs)

