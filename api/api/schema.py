import graphene
import graphql_jwt
from everecon import (schema_community, schema_event, schema_init,
                      schema_search, schema_speaker, schema_users)
from graphene_django import DjangoObjectType


class Query(schema_init.Query, schema_users.Query,
            schema_community.Query, schema_event.Query,
            schema_speaker.Query, graphene.ObjectType):
    pass


class Mutation(schema_users.Mutation, schema_community.Mutation,
               schema_event.Mutation, schema_speaker.Mutation,
               schema_search.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()
    pass

    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
