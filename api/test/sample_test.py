from graphene.test import Client


def test_unit():
    assert True


def test_hello_stranger(client: Client):
    query = """
    query{
        hello
    }
    """
    result = client.execute(query)
    assert result["data"]["hello"] == "Hello stranger"


def test_hello_name(client: Client):
    query = """
   query{
        hello(name:"arpit")
    }
    """
    result = client.execute(query)
    assert result["data"]["hello"] == "Hello arpit"
