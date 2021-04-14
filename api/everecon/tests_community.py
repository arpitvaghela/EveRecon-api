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
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

        # Clear database

    @classmethod
    def tearDown(cls):
        Category.objects.all().delete()
        Event.objects.all().delete()
        Community.objects.all().delete()
        User.objects.all().delete()

    # Create Community testing
    def test_create_community(self):
        create_community = '''
        mutation createCommunity ($address: String, $city: String, $country: String, $description: String!, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $instagram: String, $linkedin: String, $name: String!, $twitter: String, $website: String) {
            createCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, instagram: $instagram, linkedin: $linkedin, name: $name, twitter: $twitter, website: $website) {
                community{
                    address
                    city
                    country
                    description
                    discord
                    email
                    facebook
                    featuredVideo
                    instagram
                    linkedin
                    name
                    twitter
                    website
                }
            }
        }
        '''

        variables = {
            "address": "Test_address",
            "city": "Test_city",
            "country": "Test_country",
            "description": "Test_description",
            "discord": "https://discordapp.com/users/mrparth23#0639",
            "email": "Test_email",
            "facebook": "https://www.facebook.com/mrparth23/",
            "featuredVideo": "https://www.youtube.com/watch?v=OFA5UfVimxI",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "linkedin": "https://www.linkedin.com/in/mrparth23/",
            "name": "Test_community",
            "twitter": "https://twitter.com/mrparth23",
            "website": "https://www.facebook.com/"
        }

        data = {'community': {
            "address": variables['address'],
            "city": variables['city'],
            "country": variables['country'],
            "description": variables['description'],
            "discord": variables['discord'],
            "email": variables['email'],
            "facebook": variables['facebook'],
            "featuredVideo": variables['featuredVideo'],
            "instagram": variables['instagram'],
            "linkedin": variables['linkedin'],
            "name": variables['name'],
            "twitter": variables['twitter'],
            "website": variables['website']
        }}

        response = self.client.execute(create_community, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Update Community testing
    def test_update_community(self):
        community = self.create_dummy_community()
        follower = []
        follower_id = []
        for i in range(0, 5):
            user = self.create_dummy_user()
            js = {'id': str(user.id), 'username': user.username}
            follower.append(js)
            follower_id.append(user.id)

        update_community = '''
        mutation updateCommunity ($address: String, $city: String, $country: String, $description: String, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $followers: [ID], $id: ID!, $instagram: String, $isActive: Boolean, $linkedin: String, $name: String, $website: String) {
            updateCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, followers: $followers, id: $id, instagram: $instagram, isActive: $isActive, linkedin: $linkedin, name: $name, website: $website) {
                community {
                    address
                    city
                    country
                    description
                    discord
                    email
                    facebook
                    featuredVideo
                    followers {
                        id
                        username
                    }
                    isActive
                    name
                    instagram
                    linkedin
                    twitter
                    website
                }
            }
        }
        '''
        variables = {
            "address": "Test_address",
            "city": "Test_city",
            "country": "Test_country",
            "description": "Test_description",
            "discord": "https://discordapp.com/users/mrparth23#0639",
            "email": "test@gmail.com",
            "facebook": "https://www.facebook.com/mrparth23/",
            "featuredVideo": "https://www.youtube.com/watch?v=OFA5UfVimxI",
            "followers": follower_id,
            "id": community.id,
            "isActive": True,
            "name": "Test_community",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "linkedin": "https://www.linkedin.com/in/mrparth23/",
            "twitter": "https://twitter.com/mrparth23",
            "website": "https://github.com/arpitvaghela/EveRecon-api/tree/backend"
        }

        data = {'community': {
            "address": variables['address'],
            "city": variables['city'],
            "country": variables['country'],
            "description": variables['description'],
            "discord": variables['discord'],
            "email": variables['email'],
            "facebook": variables['facebook'],
            "featuredVideo": variables['featuredVideo'],
            "followers": follower,
            "isActive": variables['isActive'],
            "name": variables['name'],
            "instagram": variables['instagram'],
            "linkedin": variables['linkedin'],
            "twitter": variables['twitter'],
            "website": variables['website']
        }}

        response = self.client.execute(update_community, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Delete Community
    def test_delete_community(self):
        community = self.create_dummy_community()

        delete_community = '''
        mutation deleteCommunity ($id: ID) {
            deleteCommunity (id: $id) {
                ok
            }
        }
        '''

        variables = {
            "id": community.id
        }

        data = {'ok': True}

        response = self.client.execute(delete_community, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # CommunityByID testing
    def test_community_by_id(self):
        community = self.create_dummy_community()
        community_by_id = '''
            query communityById ($id: ID){
                 communityById(id: $id) {
                     id
                     name
                 }
             }
        '''

        variables = {
            'id': community.id,
        }

        data = {
            'id': str(variables['id']),
            'name': community.name
        }

        response = self.client.execute(community_by_id, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Add CoreMember
    def test_add_core_member(self):
        community = self.create_dummy_community()
        user = self.create_dummy_user()

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

        data = {
            "ok": True
        }

        response = self.client.execute(add_core_member, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Remove CoreMember
    def test_remove_core_member(self):
        community = self.create_dummy_community()
        user = self.create_dummy_user()

        remove_core_member = '''
            mutation removeCoreMember ($community: ID!, $user: ID!) {
                removeCoreMember (community: $community, user: $user) {
                    ok
                }
            }
            '''

        variables = {
            "community": community.id,
            "user": user.id
        }

        data = {
            "ok": True
        }

        response = self.client.execute(remove_core_member, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Add Volunteer
    def test_add_volunteer(self):
        community = self.create_dummy_community()
        user = self.create_dummy_user()

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

        data = {
            "ok": True
        }

        response = self.client.execute(add_volunteer, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Remove Volunteer
    def test_remove_volunteer(self):
        community = self.create_dummy_community()
        user = self.create_dummy_user()

        remove_volunteer = '''
            mutation removeVolunteer ($community: ID!, $user: ID!) {
                removeVolunteer (community: $community, user: $user) {
                    ok
                }
            }
            '''

        variables = {
            "community": community.id,
            "user": user.id
        }

        data = {
            "ok": True
        }

        response = self.client.execute(remove_volunteer, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Add Follower
    def test_add_follower(self):
        community = self.create_dummy_community()
        user = self.create_dummy_user()

        add_follower = '''
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

        data = {
            "ok": True
        }

        response = self.client.execute(add_follower, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Remove Follower
    def test_remove_follower(self):
        community = self.create_dummy_community()
        user = self.create_dummy_user()

        remove_follower = '''
            mutation removeVolunteer ($community: ID!, $user: ID!) {
                removeVolunteer (community: $community, user: $user) {
                    ok
                }
            }
            '''

        variables = {
            "community": community.id,
            "user": user.id
        }

        data = {
            "ok": True
        }

        response = self.client.execute(remove_follower, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)