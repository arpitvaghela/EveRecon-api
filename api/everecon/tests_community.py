from .models import *
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import sys

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
        self.user = get_user_model().objects.create(username='test', password='Test@10')
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
                community {
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
            "email": "Test@gmail.com",
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
        self.assertNotIn('errors', response.to_dict())
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
        self.assertNotIn('errors', response.to_dict())
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
        self.assertNotIn('errors', response.to_dict())
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
        self.assertNotIn('errors', response.to_dict())
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
        self.assertNotIn('errors', response.to_dict())
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
        self.assertNotIn('errors', response.to_dict())
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
        self.assertNotIn('errors', response.to_dict())
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
        self.assertNotIn('errors', response.to_dict())
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
        self.assertNotIn('errors', response.to_dict())
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
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Invalid EmailID in create community
    def test_create_community_email_validation(self):
        create_community_email = '''
        mutation createCommunity ($address: String, $city: String, $country: String, $description: String!, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $instagram: String, $linkedin: String, $name: String!, $twitter: String, $website: String) {
            createCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, instagram: $instagram, linkedin: $linkedin, name: $name, twitter: $twitter, website: $website) {
                community{
                    email
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
            "facebook": "https://www.facebook.com/mr.parth23/",
            "featuredVideo": "https://www.youtube.com/watch?v=OFA5UfVimxI",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "linkedin": "https://www.linkedin.com/in/mrparth23/",
            "name": "Test_community",
            "twitter": "https://twitter.com/mrparth23",
            "website": "https://www.facebook.com/"
        }

        response = self.client.execute(create_community_email, variables)
        self.assertIn('errors', response.to_dict())

    # Facebook validation test in createCommunity
    def test_create_community_facebook_validation(self):
        create_community_facebook = '''
        mutation createCommunity ($address: String, $city: String, $country: String, $description: String!, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $instagram: String, $linkedin: String, $name: String!, $twitter: String, $website: String) {
            createCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, instagram: $instagram, linkedin: $linkedin, name: $name, twitter: $twitter, website: $website) {
                community{
                    facebook
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
            "facebook": "https://www.instagram.com/mr.parth23/",
            "featuredVideo": "https://www.youtube.com/watch?v=OFA5UfVimxI",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "linkedin": "https://www.linkedin.com/in/mrparth23/",
            "name": "Test_community",
            "twitter": "https://twitter.com/mrparth23",
            "website": "https://www.facebook.com/"
        }

        response = self.client.execute(create_community_facebook, variables)
        self.assertIn('errors', response.to_dict())

    # Instagram validation test in createCommunity
    def test_create_community_instagram_validation(self):
        create_community_instagram = '''
        mutation createCommunity ($address: String, $city: String, $country: String, $description: String!, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $instagram: String, $linkedin: String, $name: String!, $twitter: String, $website: String) {
            createCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, instagram: $instagram, linkedin: $linkedin, name: $name, twitter: $twitter, website: $website) {
                community{
                    instagram
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
            "facebook": "https://www.facebook.com/mr.parth23/",
            "featuredVideo": "https://www.youtube.com/watch?v=OFA5UfVimxI",
            "instagram": "https://www.facebook.com/mr.parth23/",
            "linkedin": "https://www.linkedin.com/in/mrparth23/",
            "name": "Test_community",
            "twitter": "https://twitter.com/mrparth23",
            "website": "https://www.facebook.com/"
        }

        response = self.client.execute(create_community_instagram, variables)
        self.assertIn('errors', response.to_dict())

    # Discord validation test in createCommunity
    def test_create_community_discord_validation(self):
        create_community_discord = '''
        mutation createCommunity ($address: String, $city: String, $country: String, $description: String!, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $instagram: String, $linkedin: String, $name: String!, $twitter: String, $website: String) {
            createCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, instagram: $instagram, linkedin: $linkedin, name: $name, twitter: $twitter, website: $website) {
                community{
                    discord
                }
            }
        }
        '''

        variables = {
            "address": "Test_address",
            "city": "Test_city",
            "country": "Test_country",
            "description": "Test_description",
            "discord": "test",
            "email": "test@gmail.com",
            "facebook": "https://www.facebook.com/mr.parth23/",
            "featuredVideo": "https://www.youtube.com/watch?v=OFA5UfVimxI",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "linkedin": "https://www.linkedin.com/in/mrparth23/",
            "name": "Test_community",
            "twitter": "https://twitter.com/mrparth23",
            "website": "https://www.facebook.com/"
        }

        response = self.client.execute(create_community_discord, variables)
        self.assertIn('errors', response.to_dict())

    # Youtube validation test in createCommunity
    def test_create_community_youtube_validation(self):
        create_community_youtube = '''
        mutation createCommunity ($address: String, $city: String, $country: String, $description: String!, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $instagram: String, $linkedin: String, $name: String!, $twitter: String, $website: String) {
            createCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, instagram: $instagram, linkedin: $linkedin, name: $name, twitter: $twitter, website: $website) {
                community{
                    featuredVideo
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
            "facebook": "https://www.facebook.com/mr.parth23/",
            "featuredVideo": "https://discordapp.com/users/mrparth23#0639",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "linkedin": "https://www.linkedin.com/in/mrparth23/",
            "name": "Test_community",
            "twitter": "https://twitter.com/mrparth23",
            "website": "https://www.facebook.com/"
        }

        response = self.client.execute(create_community_youtube, variables)
        self.assertIn('errors', response.to_dict())

    # linkedin validation test in createCommunity
    def test_create_community_linkedin_validation(self):
        create_community_linkedin = '''
        mutation createCommunity ($address: String, $city: String, $country: String, $description: String!, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $instagram: String, $linkedin: String, $name: String!, $twitter: String, $website: String) {
            createCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, instagram: $instagram, linkedin: $linkedin, name: $name, twitter: $twitter, website: $website) {
                community{
                    linkedin
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
            "facebook": "https://www.facebook.com/mr.parth23/",
            "featuredVideo": "https://www.youtube.com/watch?v=OFA5UfVimxI",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "linkedin": "https://www.instagram.com/mr.parth23/",
            "name": "Test_community",
            "twitter": "https://twitter.com/mrparth23",
            "website": "https://www.facebook.com/"
        }

        response = self.client.execute(create_community_linkedin, variables)
        self.assertIn('errors', response.to_dict())

    # Twitter validation test in createCommunity
    def test_create_community_twitter_validation(self):
        create_community_twitter = '''
        mutation createCommunity ($address: String, $city: String, $country: String, $description: String!, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $instagram: String, $linkedin: String, $name: String!, $twitter: String, $website: String) {
            createCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, instagram: $instagram, linkedin: $linkedin, name: $name, twitter: $twitter, website: $website) {
                community{
                    twitter
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
            "facebook": "https://www.facebook.com/mr.parth23/",
            "featuredVideo": "https://www.youtube.com/watch?v=OFA5UfVimxI",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "linkedin": "https://www.linkedin.com/in/mrparth23/",
            "name": "Test_community",
            "twitter": "https://www.facebook.com/mr.parth23/",
            "website": "https://www.facebook.com/"
        }

        response = self.client.execute(create_community_twitter, variables)
        self.assertIn('errors', response.to_dict())

    # Create community without required field
    def test_create_community_without_desc(self):
        create_community = '''
        mutation createCommunity ($address: String, $city: String, $country: String, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $instagram: String, $linkedin: String, $name: String!, $twitter: String, $website: String) {
            createCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, instagram: $instagram, linkedin: $linkedin, name: $name, twitter: $twitter, website: $website) {
                community{
                    name
                }
            }
        }
        '''

        variables = {
            "address": "Test_address",
            "city": "Test_city",
            "country": "Test_country",
            "discord": "ayush",
            "email": "Test_email",
            "facebook": "https://www.facebook.com/mr.parth23/",
            "featuredVideo": "https://www.facebook.com/",
            "instagram": "https://www.facebook.com/mr.parth23/",
            "linkedin": "https://www.facebook.com/",
            "name": "Test_community",
            "twitter": "https://www.facebook.com/",
            "website": "https://www.facebook.com/"
        }

        response = self.client.execute(create_community, variables)
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