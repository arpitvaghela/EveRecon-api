import graphene
from graphene_django import DjangoObjectType
from everecon import schema_init


class Query(schema_init.Query,  graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    pass

    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query)
