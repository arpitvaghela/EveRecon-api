import graphene
from django.test.testcases import TestCase

from .schema import Query


class InitTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.query = """
        query{
            foo
        }
        """

    def test_foo(self):
        schema = graphene.Schema(query=Query)
        result = schema.execute(self.query)
        self.assertIsNone(result.errors)
        self.assertDictEqual({"foo": "Hello, World!"}, result.data)
