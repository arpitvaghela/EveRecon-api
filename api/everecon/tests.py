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

    def create_dummy_event(self):
        community = self.create_dummy_community()
        category = self.create_dummy_category()
        date_time = datetime.now()
        event = Event.objects.create(
            name="Test_event",
            address="Test_address",
            category=category,
            city="Test_city",
            community=community,
            country="Test_country",
            description="Test_description",
            end_time=date_time,
            kind="Virtual",
            live_URL="https://github.com/arpitvaghela/EveRecon-api",
            max_RSVP=50,
            start_time=date_time
        )
        # event.tags.set(["Test_tag1", "Test_tag2"])
        # event.save()
        return event

    def create_dummy_speaker(self):
        return Speaker.objects.create(
            description="Test_Description",
            email="test@gmail.com",
            facebook="https://www.facebook.com/mrparth23/",
            first_name="Test_firstname",
            instagram="https://www.instagram.com/mr.parth23/",
            last_name="Test_lastname"
        )

    def create_dummy_category(self):
        return Category.objects.create(name="Test_category")

    def setUp(self):
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    # Create User
    def test_create_user(self):
        create_user = '''
        mutation createUser ($city: String, $contact: String, $country: String, $email: String!, $password: String!, $username: String!) {
            createUser (city: $city, contact: $contact, country: $country, email: $email, password: $password, username: $username) {
                user {
                    id
                    username
                }
            }
        }
        '''

        variables_create_user = {
            "city": "Test_city",
            "contact": "9876543210",
            "country": "Test_country",
            "email": "Test_email",
            "password": "Test_password",
            "username": "Test_username"
        }

        exe_create_user = self.client.execute(create_user, variables_create_user)
        print("\nThis is createUser testing : ")
        print(exe_create_user.to_dict())

    # Token Auth
    def test_token_auth(self):
        user = self.create_dummy_user()

        token_auth = '''
        mutation tokenAuth ($username: String!, $password: String!) {
            tokenAuth (username: $username, password: $password) {
                token
                refreshToken
            }
        }
        '''

        # hard coded works, issue to be solved
        # error : raise exceptions.JSONWebTokenError( graphql.error.located_error.GraphQLLocatedError:
        #           Please, enter valid credentials

        variables_token_auth = {
            "username": user.username,
            "password": user.password
        }

        exe_token_auth = self.client.execute(token_auth, variables_token_auth)
        print("\nThis is tokenAuth testing : ")
        print(exe_token_auth.to_dict())

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
        print("\nThis is refreshToken testing : ")
        print(exe_refresh_token.to_dict())

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
        print("\nThis is verifyToken testing : ")
        print(exe_verify_token.to_dict())

    # Create Community testing
    def test_create_community(self):
        create_community = '''
        mutation createCommunity ($address: String, $city: String, $country: String, $description: String!, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $instagram: String, $linkedin: String, $name: String!, $twitter: String, $website: String) {
            createCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, instagram: $instagram, linkedin: $linkedin, name: $name, twitter: $twitter, website: $website) {
                community{
                    id
                    name
                }
                leader {
                    id
                    username
                }
            }
        }
        '''

        variables_create_community = {
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

        exe_create_community = self.client.execute(create_community, variables_create_community)
        print("\nThis is createCommunity testing : ")
        print(exe_create_community.to_dict())

    # Update Community testing
    def test_update_community(self):
        community = self.create_dummy_community()
        update_community = '''
        mutation updateCommunity ($address: String, $city: String, $country: String, $description: String, $discord: String, $email: String, $facebook: String, $featuredVideo: String, $followers: [ID], $id: ID!, $instagram: String, $isActive: Boolean, $linkedin: String, $name: String, $website: String) {
            updateCommunity (address: $address, city: $city, country: $country, description: $description, discord: $discord, email: $email, facebook: $facebook, featuredVideo: $featuredVideo, followers: $followers, id: $id, instagram: $instagram, isActive: $isActive, linkedin: $linkedin, name: $name, website: $website) {
                community {
                    id
                    name
                }
            }
        }
        '''
        variables_update_community = {
            "address": "Test_address",
            "city": "Test_city",
            "country": "Test_country",
            "description": "Test_description",
            "discord": "https://discordapp.com/users/mrparth23#0639",
            "email": "test@gmail.com",
            "facebook": "https://www.facebook.com/mrparth23/",
            "featuredVideo": "https://www.youtube.com/watch?v=OFA5UfVimxI",
            "followers": [
                0
            ],
            "id": community.id,
            "isActive": True,
            "name": "Test_community",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "linkedin": "https://www.linkedin.com/in/mrparth23/",
            "twitter": "https://twitter.com/mrparth23",
            "website": "https://github.com/arpitvaghela/EveRecon-api/tree/backend"
        }

        exe_update_community = self.client.execute(update_community, variables_update_community)
        print("\nThis is updateCommunity testing : ")
        print(exe_update_community.to_dict())

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

        variables_delete_community = {
            "id": community.id
        }

        exe_delete_community = self.client.execute(delete_community, variables_delete_community)
        print("\nThis is deleteCommunity testing : ")
        print(exe_delete_community.to_dict())

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

        variables_community_by_id = {
            'id': community.id
        }

        exe_community_by_id = self.client.execute(community_by_id, variables_community_by_id)
        print("\nThis is communityById testing : ")
        print(exe_community_by_id.to_dict())

    # Create Event
    def test_create_event(self):
        community = self.create_dummy_community()
        category = self.create_dummy_category()
        date_time = datetime.now()

        create_event = '''
        mutation createEvent ($address: String, $category: ID!, $city: String, $community: ID, $country: String, $description: String!, $endTime: DateTime!, $kind: String!, $liveUrl: String, $maxRsvp: Int, $name: String!, $startTime: DateTime!, $tags: [String]) {
            createEvent (address: $address, category: $category, city: $city, community: $community, country: $country, description: $description, endTime: $endTime, kind: $kind, liveUrl: $liveUrl, maxRsvp: $maxRsvp, name: $name, startTime: $startTime, tags: $tags) {
                event {
                    id
                    name
                }
            }
        }
        '''

        variables_create_event = {
            "address": "Test_address",
            "category": category.id,
            "city": "Test_city",
            "community": community.id,
            "country": "Test_country",
            "description": "Test_description",
            "endTime": date_time,
            "kind": "Virtual",
            "liveUrl": "https://github.com/arpitvaghela/EveRecon-api",
            "maxRsvp": 50,
            "name": "Test_event",
            "startTime": date_time,
            "tags": ["Test_tag1", "Test_tag2"]
        }

        exe_create_event = self.client.execute(create_event, variables_create_event)
        print("\nThis is createEvent testing : ")
        print(exe_create_event.to_dict())

    # Update event
    def test_update_event(self):
        event = self.create_dummy_event()
        community = Community.objects.get(id=event.community.id)
        category = Category.objects.get(id=event.category.id)
        date_time = datetime.now()

        update_event = '''
        mutation updateEvent ($address: String, $category: ID, $city: String, $country: String, $description: String, $endTime: DateTime, $id: ID!, $kind: String, $liveUrl: String, $maxRsvp: Int, $name: String, $startTime: DateTime, $tags: [String]) {
            updateEvent (address: $address, category: $category, city: $city, country: $country, description: $description, endTime: $endTime, id: $id, kind: $kind, liveUrl: $liveUrl, maxRsvp: $maxRsvp, name: $name, startTime: $startTime, tags: $tags) {
                event {
                    id
                    name
                }
            }
        }
        '''

        variables_update_event = {
            "address": "Test_address",
            "category": category.id,
            "city": "Test_city",
            "community": community.id,
            "country": "Test_country",
            "description": "Test_description",
            "endTime": date_time,
            "kind": "Virtual",
            "liveUrl": "https://github.com/arpitvaghela/EveRecon-api/tree/backend",
            "maxRsvp": 50,
            "id": event.id,
            "name": "Test_event",
            "startTime": date_time,
            "tags": ["Test_tag1", "Test_tag2"]
        }

        exe_update_event = self.client.execute(update_event, variables_update_event)
        print("\nThis is updateEvent testing : ")
        print(exe_update_event.to_dict())

    # Delete Event
    def test_delete_event(self):
        event = self.create_dummy_event()

        delete_event = '''
            mutation deleteEvent ($id: ID) {
            deleteEvent (id: $id) {
                ok
            }
        }
        '''

        variables_delete_event = {
            "id": event.id
        }

        exe_delete_event = self.client.execute(delete_event, variables_delete_event)
        print("\nThis is deleteEvent testing : ")
        print(exe_delete_event.to_dict())

    # Register Event
    def test_register_event(self):
        event = self.create_dummy_event()

        register_event = '''
        mutation registerEvent ($id: ID!) {
            registerEvent (id: $id) {
                event {
                    id
                    name
                }  
            }
        }
        '''

        variables_register_event = {
            "id": event.id
        }

        exe_register_event = self.client.execute(register_event, variables_register_event)
        print("\nThis is registerEvent testing : ")
        print(exe_register_event.to_dict())

    # EventByID testing
    def test_event_by_id(self):
        event = self.create_dummy_event()
        event_by_id = '''
            query eventById ($id: ID){
                 eventById(id: $id) {
                     id
                     name
                 }
             }
        '''

        variables_event_by_id = {
            'id': event.id
        }

        exe_event_by_id = self.client.execute(event_by_id, variables_event_by_id)
        print("\nThis is eventById testing : ")
        print(exe_event_by_id.to_dict())

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

        variables_add_core_member = {
            "community": community.id,
            "user": user.id
        }

        exe_add_core_member = self.client.execute(add_core_member, variables_add_core_member)
        print("\nThis is addCoreMember testing : ")
        print(exe_add_core_member.to_dict())

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

        variables_remove_core_member = {
            "community": community.id,
            "user": user.id
        }

        exe_remove_core_member = self.client.execute(remove_core_member, variables_remove_core_member)
        print("\nThis is removeCoreMember testing : ")
        print(exe_remove_core_member.to_dict())

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

        variables_add_volunteer = {
            "community": community.id,
            "user": user.id
        }

        exe_add_volunteer = self.client.execute(add_volunteer, variables_add_volunteer)
        print("\nThis is addVolunteer testing : ")
        print(exe_add_volunteer.to_dict())

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

        variables_remove_volunteer = {
            "community": community.id,
            "user": user.id
        }

        exe_remove_volunteer = self.client.execute(remove_volunteer, variables_remove_volunteer)
        print("\nThis is removeVolunteer testing : ")
        print(exe_remove_volunteer.to_dict())

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

        variables_add_follower = {
            "community": community.id,
            "user": user.id
        }

        exe_add_follower = self.client.execute(add_follower, variables_add_follower)
        print("\nThis is addFollower testing : ")
        print(exe_add_follower.to_dict())

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

        variables_remove_follower = {
            "community": community.id,
            "user": user.id
        }

        exe_remove_follower = self.client.execute(remove_follower, variables_remove_follower)
        print("\nThis is removeFollower testing : ")
        print(exe_remove_follower.to_dict())

    # Create Speaker
    def test_create_speaker(self):
        create_speaker = '''
        mutation createSpeaker ($description: String, $email: String, $facebook: String, $firstName: String!, $instagram: String, $lastName: String) {
            createSpeaker (description: $description, email: $email, facebook: $facebook, firstName: $firstName, instagram: $instagram, lastName: $lastName) {
                speaker {
                    id
                    firstName
                    lastName
                }
            }
        }
        '''

        variables_create_speaker = {
            "description": "Test_Description",
            "email": "test@gmail.com",
            "facebook": "https://www.facebook.com/mrparth23/",
            "firstName": "Test_firstname",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "lastName": "Test_lastname"
        }

        exe_create_speaker = self.client.execute(create_speaker, variables_create_speaker)
        print("\nThis is createSpeaker testing : ")
        print(exe_create_speaker.to_dict())

    # Add Speaker
    def test_add_speaker(self):
        event = self.create_dummy_event()
        speaker = self.create_dummy_speaker()

        add_speaker = '''
        mutation addSpeaker ($eventid: ID!, $speakerid: ID!) {
            addSpeaker (eventid: $eventid, speakerid: $speakerid) {
                ok
            }
        }
        '''

        variables_add_speaker = {
            "eventid": event.id,
            "speakerid": speaker.id
        }

        exe_add_speaker = self.client.execute(add_speaker, variables_add_speaker)
        print("\nThis is addSpeaker testing : ")
        print(exe_add_speaker.to_dict())

    # Remove Speaker
    def test_remove_speaker(self):
        event = self.create_dummy_event()
        speaker = self.create_dummy_speaker()

        remove_speaker = '''
        mutation removeSpeaker ($eventid: ID!, $speakerid: ID!) {
            removeSpeaker (eventid: $eventid, speakerid: $speakerid) {
                ok
            }
        }
        '''

        variables_remove_speaker = {
            "eventid": event.id,
            "speakerid": speaker.id
        }

        exe_remove_speaker = self.client.execute(remove_speaker, variables_remove_speaker)
        print("\nThis is removeSpeaker testing : ")
        print(exe_remove_speaker.to_dict())

    # Clear database
    def tearDown(self):
        Category.objects.all().delete()
        Event.objects.all().delete()
        Community.objects.all().delete()
        User.objects.all().delete()