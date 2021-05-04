import sys

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase

from .models import *

sys.tracebacklimit = 0

GraphQLTestCase.GRAPHQL_URL = "http://127.0.0.1:8000/graphql/"
print(GraphQLTestCase.GRAPHQL_URL)

global id
id = 1


class EveReconTest(JSONWebTokenTestCase):

    def create_dummy_user(self):
        global id
        user = User.objects.create(
            username="Test_username_" + str(id),
            password="Test_password@" + str(id),
            email="test@gmail.com",
        )
        user.set_password("Test_password")
        user.save()
        id += 1
        return user

    def create_dummy_community(self):
        user = self.create_dummy_user()
        return Community.objects.create(
            name="Test_community",
            address="Test_address",
            city="Test_city",
            country="Test_country",
            description="Test_description",
            discord="https://discordapp.com/users/mrparth23#0639",
            email="test@gmail.com",
            facebook="https://www.facebook.com/mrparth23/",
            featured_video="https://www.youtube.com/watch?v=OFA5UfVimxI",
            instagram="https://www.instagram.com/mr.parth23/",
            linkedin="https://www.linkedin.com/in/mrparth23/",
            twitter="https://twitter.com/mrparth23",
            website="https://www.facebook.com/",
            leader=user
        )

    def setUp(self):
        self.user = get_user_model().objects.create(username='test', password="Test@10", email="test@gmail.com")
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
        mutation createUser ($city: String, $contact: String, $country: String, $email: String!, $firstname: String, $lastname: String, $password: String!, $username: String!) {
            createUser (city: $city, contact: $contact, country: $country, email: $email, firstname: $firstname, lastname: $lastname, password: $password, username: $username) {
                user {
                    profile{
                        city
                        contact
                        country
                    }
                    email
                    username
                    firstName
                    lastName
                }
            }
        }
        '''

        variables = {
            "city": "Test_city",
            "contact": "9876543210",
            "country": "Test_country",
            "email": "Test@gmail.com",
            "password": "Test_password",
            "username": "Test_username",
            "firstname": "Test_firstname",
            "lastname": "Test_lastname"
        }

        data = {'user': {
            "profile": {
                "city": variables['city'],
                "contact": variables['contact'],
                "country": variables['country']
            },
            'email': variables['email'],
            'username': variables['username'],
            'firstName': variables['firstname'],
            'lastName': variables['lastname']
        }}

        response = self.client.execute(create_user, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Token Auth
    def test_token_auth(self):
        user = get_user_model()(
            username='Test_username',
            email='test@gmail.com',
        )
        user.set_password("Test_password@123")
        user.save()

        token_auth = '''
        mutation tokenAuth ($username: String!, $password: String!) {
            tokenAuth (username: $username, password: $password) {
                token
                refreshToken
            }
        }
        '''

        variables_token_auth = {
            'username': 'Test_username',
            'password': 'Test_password@123'
        }

        exe_token_auth = self.client.execute(token_auth, variables_token_auth)
        self.assertNotIn('errors', exe_token_auth.to_dict())

        # Refresh token
        refresh_token = '''
                mutation refreshToken ($refreshToken: String!) {
                    refreshToken (refreshToken: $refreshToken) {
                        token
                        payload
                        refreshToken
                    }
                }
                '''

        variables_refresh_token = {
            "refreshToken": exe_token_auth.to_dict()['data']['tokenAuth']['refreshToken']
        }

        exe_refresh_token = self.client.execute(refresh_token, variables_refresh_token)
        self.assertNotIn('errors', exe_token_auth.to_dict())

        # Verify token
        verify_token = '''
        mutation verifyToken ($token: String!) {
            verifyToken (token: $token) {
                payload
            }
        }
        '''

        variables_verify_token = {
            "token": exe_token_auth.to_dict()['data']['tokenAuth']['token']
        }

        exe_verify_token = self.client.execute(verify_token, variables_verify_token)
        self.assertNotIn('errors', exe_token_auth.to_dict())

    # WhoAmI
    def test_whoami(self):
        myprofile = self.create_dummy_user()
        self.client.authenticate(myprofile)
        whoami = '''
            query whoami {
                whoami{
                    username
                    email           
                }

            }
        '''
        data = {
            'username': myprofile.username,
            'email': myprofile.email
        }
        response = self.client.execute(whoami)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # My profile
    def test_my_profile(self):
        myprofile = self.create_dummy_user()
        self.client.authenticate(myprofile)

        myprofile_query = '''
            query myprofile {
                myprofile{
                    username
                    email
                }
            }        
        '''
        data = {
            'username': myprofile.username,
            'email': myprofile.email
        }
        response = self.client.execute(myprofile_query)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # user by username
    def test_user_by_username(self):
        user = self.create_dummy_user()

        userbyUsername = '''
        query userByName($username:String!) {
            userByName(username:$username) {
                id
                username
                email
               }
        }
        '''

        variables = {
            'username': user.username
        }

        data = {
            'id': str(user.id),
            'username': user.username,
            'email': user.email
        }

        response = self.client.execute(userbyUsername, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Update user
    def test_update_user(self):
        user = self.create_dummy_user()
        self.client.authenticate(user)

        updateUser = '''
        mutation updateUser ($firstname: String, $lastname: String, $city: String, $contact: String, $country: String) {
            updateUser (firstname: $firstname, lastname: $lastname, city: $city, contact: $contact, country: $country) {
                profile {
                    id
                    contact
                    city
                    country
                }
                user {
                    id
                    username
                }    
            }
        }
        '''

        variables = {
            "firstname": "Test_firstname",
            "lastname": "Test_lastname",
            "city": "Test_city",
            "contact": "9824169356",
            "country": "Test_country"
        }

        data = {
            'profile': {
                'id': str(user.id),
                'contact': variables['contact'],
                'city': variables['city'],
                'country': variables['country']
            },
            'user': {
                'id': str(user.id),
                'username': user.username
            }
        }

        response = self.client.execute(updateUser, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # User role dependencies(Core Member/ Volunteer)
    def test_volunteer_as_core_member(self):
        try:
            with transaction.atomic():
                user = self.create_dummy_user()
                community = self.create_dummy_community()

                add_core_member = '''
                    mutation addCoreMember ($community: ID!, $user: ID!) {
                        addCoreMember (community: $community, user: $user) {
                            ok
                        }
                    }
                '''

                add_volunteer = '''
                    mutation addVolunteer ($community: ID!, $user: ID!) {
                        addVolunteer (community: $community, user: $user) {
                            ok
                        }
                    }
                '''

                variables = {
                    "community": community.id,
                    "user": user.id
                }

                response = self.client.execute(add_core_member, variables)
                self.assertNotIn('errors', response.to_dict())

                response1 = self.client.execute(add_volunteer, variables)
                self.assertIn('errors', response1.to_dict())

        except IntegrityError:
            pass

    # User role dependencies(Core Member/ Volunteer)
    def test_core_member_as_volunteer(self):
        try:
            with transaction.atomic():
                user = self.create_dummy_user()
                community = self.create_dummy_community()

                add_volunteer = '''
                    mutation addVolunteer ($community: ID!, $user: ID!) {
                        addVolunteer (community: $community, user: $user) {
                            ok
                        }
                    }
                '''

                add_core_member = '''
                    mutation addCoreMember ($community: ID!, $user: ID!) {
                        addCoreMember (community: $community, user: $user) {
                            ok
                        }
                    }
                '''

                variables = {
                    "community": community.id,
                    "user": user.id
                }

                response = self.client.execute(add_volunteer, variables)
                self.assertNotIn('errors', response.to_dict())

                response1 = self.client.execute(add_core_member, variables)
                self.assertIn('errors', response1.to_dict())

        except IntegrityError:
            pass

    # User role dependencies(Core Member/ Volunteer)
    def test_volunteer_as_leader(self):
        try:
            with transaction.atomic():
                community = self.create_dummy_community()

                add_volunteer = '''
                    mutation addVolunteer ($community: ID!, $user: ID!) {
                        addVolunteer (community: $community, user: $user) {
                            ok
                        }
                    }
                '''

                variables = {
                    "community": community.id,
                    "user": community.leader.id
                }

                response = self.client.execute(add_volunteer, variables)
                self.assertIn('errors', response.to_dict())

        except IntegrityError:
            pass

    # User role dependencies(Core Member/ Volunteer)
    def test_core_member_as_leader(self):
        try:
            with transaction.atomic():
                community = self.create_dummy_community()

                add_core_member = '''
                    mutation addCoreMember ($community: ID!, $user: ID!) {
                        addCoreMember (community: $community, user: $user) {
                            ok
                        }
                    }
                '''

                variables = {
                    "community": community.id,
                    "user": community.leader.id
                }

                response = self.client.execute(add_core_member, variables)
                self.assertIn('errors', response.to_dict())

        except IntegrityError:
            pass

    # Contact validation test in createUser
    def test_create_user_contact_validation(self):
        create_user_contact = '''
                mutation createUser ($city: String, $contact: String, $country: String, $email: String!, $firstname: String, $lastname: String, $password: String!, $username: String!) {
                    createUser (city: $city, contact: $contact, country: $country, email: $email, firstname: $firstname, lastname: $lastname, password: $password, username: $username) {
                        user {
                            profile{
                                contact
                            }
                            username
                        }
                    }
                }
                '''

        variables = {
            "city": "Test_city",
            "contact": "98765432100",
            "country": "Test_country",
            "email": "Test@gmail.com",
            "password": "Test_password",
            "username": "Test_username",
            "firstname": "Test_firstname",
            "lastname": "Test_lastname"
        }

        response = self.client.execute(create_user_contact, variables)
        self.assertIn('errors', response.to_dict())

    # My community
    def test_my_community(self):
        myprofile = self.create_dummy_user()
        self.client.authenticate(myprofile)
        community = []
        comm = self.create_dummy_community()
        community.append({'id': str(comm.id), 'name': comm.name, 'description': comm.description})

        follow_community = '''
            mutation addFollower ($community: ID!, $user: ID!) {
                addFollower (community: $community, user: $user) {
                    ok
                }
            }
            '''
        variables = {
            "community": str(comm.id),
            "user": myprofile.id
        }

        self.client.execute(follow_community, variables)
        my_community = '''
                query myprofile {
                myprofile {
                    communities {
                        id
                        name
                        description   
                    }

                }
            }        
            '''
        data = {
            'communities': community
        }
        response = self.client.execute(my_community)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)
    
    # Invalid EmailID in create user
    def test_create_user(self):
        create_user_email = '''
        mutation createUser ($city: String, $contact: String, $country: String, $email: String!, $firstname: String, $lastname: String, $password: String!, $username: String!) {
            createUser (city: $city, contact: $contact, country: $country, email: $email, firstname: $firstname, lastname: $lastname, password: $password, username: $username) {
                user {
                    email
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
            "username": "Test_username",
            "firstname": "Test_firstname",
            "lastname": "Test_lastname"
        }

        response = self.client.execute(create_user_email, variables)
        self.assertIn('errors', response.to_dict())