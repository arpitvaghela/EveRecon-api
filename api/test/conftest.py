import pytest
import graphene
from graphene.test import Client

from ..main import Query


@pytest.fixture
def client():
    return Client(schema=graphene.Schema(query=Query))
