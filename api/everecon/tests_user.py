from django.test import TestCase
import json
import graphene
from graphene.test import Client
from datetime import datetime
from .models import *
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

GraphQLTestCase.GRAPHQL_URL = "http://127.0.0.1:8000/graphql/"
print(GraphQLTestCase.GRAPHQL_URL)

global id
id = 1


class EveReconTest(JSONWebTokenTestCase):

    def create_dummy_user(self):
        global id
        user = User.objects.create(
            username="Test_username_" + str(id),
            email="test@gmail.com",
        )
        user.set_password("Test_password")
        user.save()
        id += 1
        return user

    def setUp(self):
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    # Clear database
    @classmethod
    def tearDown(cls):
        Category.objects.all().delete()
        Event.objects.all().delete()
        Community.objects.all().delete()
        User.objects.all().delete()

    # Create User
    def test_create_user(self):
        create_user = '''
        mutation createUser ($city: String, $contact: String, $country: String, $email: String!, $password: String!, $username: String!) {
            createUser (city: $city, contact: $contact, country: $country, email: $email, password: $password, username: $username) {
                user {
                    profile{
                        city
                        contact
                        country
                    }
                    email
                    username
                }
            }
        }
        '''

        variables = {
            "city": "Test_city",
            "contact": "9876543210",
            "country": "Test_country",
            "email": "Test_email",
            "password": "Test_password",
            "username": "Test_username"
        }

        data = {'user': {
            "profile": {
                "city": variables['city'],
                "contact": variables['contact'],
                "country": variables['country']
            },
            'email': variables['email'],
            'username': variables['username']
        }}

        response = self.client.execute(create_user, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # # Token Auth
    # def test_token_auth(self):
    #     user = self.create_dummy_user()
    #
    #     token_auth = '''
    #     mutation tokenAuth ($username: String!, $password: String!) {
    #         tokenAuth (username: $username, password: $password) {
    #             token
    #             refreshToken
    #         }
    #     }
    #     '''
    #
    #     # hard coded works, issue to be solved
    #     # error : raise exceptions.JSONWebTokenError( graphql.error.located_error.GraphQLLocatedError:
    #     #           Please, enter valid credentials
    #
    #     variables_token_auth = {
    #         "username": user.username,
    #         "password": user.password
    #     }
    #
    #     exe_token_auth = self.client.execute(token_auth, variables_token_auth)
    #     print(exe_token_auth.data)
    #     print("\nThis is tokenAuth testing : ")
    #     print(exe_token_auth.to_dict())
    #
    #     # Refresh token
    #     refresh_token = '''
    #             mutation refreshToken ($refreshToken: String!) {
    #                 refreshToken (refreshToken: $refreshToken) {
    #                     token
    #                     payload
    #                     refreshToken
    #                 }
    #             }
    #             '''
    #
    #     variables_refresh_token = {
    #         "refreshToken": exe_token_auth.to_dict()['data']['tokenAuth']['refreshToken']
    #     }
    #
    #     exe_refresh_token = self.client.execute(refresh_token, variables_refresh_token)
    #     print("\nThis is refreshToken testing : ")
    #     print(exe_refresh_token.to_dict())
    #
    #     # Verify token
    #     verify_token = '''
    #     mutation verifyToken ($token: String!) {
    #         verifyToken (token: $token) {
    #             payload
    #         }
    #     }
    #     '''
    #
    #     variables_verify_token = {
    #         "token": exe_token_auth.to_dict()['data']['tokenAuth']['token']
    #     }
    #
    #     exe_verify_token = self.client.execute(verify_token, variables_verify_token)
    #     print("\nThis is verifyToken testing : ")
    #     print(exe_verify_token.to_dict())