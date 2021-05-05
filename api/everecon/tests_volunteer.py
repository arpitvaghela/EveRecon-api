import time
import pytz
from django.contrib.auth import get_user_model
from django.utils import dateparse
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
        community = Community.objects.create(
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
        # core_member
        core_members = []
        for user in range(0, 5):
            core_member = self.create_dummy_user()
            core_members.append(core_member)
        community.core_members.set(core_members)
        # volunteer
        volunteers = []
        for user in range(0, 5):
            volunteer = self.create_dummy_user()
            volunteers.append(volunteer)
        community.volunteers.set(volunteers)
        return community

    def create_dummy_event(self):
        community = self.create_dummy_community()
        category = self.create_dummy_category()

        start_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))
        time.sleep(2)
        end_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))

        event = Event.objects.create(
            name="Test_event",
            address="Test_address",
            category=category,
            city="Test_city",
            community=community,
            country="Test_country",
            description="Test_description",
            end_time=end_time,
            kind="V",
            live_URL="https://github.com/arpitvaghela/EveRecon-api",
            max_RSVP=50,
            start_time=start_time
        )
        return event

    def create_dummy_speaker(self):
        return Speaker.objects.create(
            description="Test_Description",
            email="test@gmail.com",
            facebook='https://www.facebook.com/mrparth23/',
            first_name="Test_firstname",
            instagram="https://www.instagram.com/mr.parth23/",
            last_name="Test_lastname"
        )

    def create_dummy_category(self):
        global id
        category = Category.objects.create(name="Test_category_" + str(id))
        category.save()
        id += 1
        return category

    def setUp(self):
        self.user = get_user_model().objects.create(username='test', password="Test@10")
        self.client.authenticate(self.user)

    # Clear database
    @classmethod
    def tearDown(cls):
        Category.objects.all().delete()
        Event.objects.all().delete()
        Community.objects.all().delete()
        User.objects.all().delete()

    # Update Community testing
    def test_update_community(self):
        follower = []
        follower_id = []
        for i in range(0, 5):
            user = self.create_dummy_user()
            js = {'id': str(user.id), 'username': user.username}
            follower.append(js)
            follower_id.append(user.id)

        community = self.create_dummy_community()
        volunteers = community.volunteers.all()
        self.client.authenticate(volunteers[0])

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

        response = self.client.execute(update_community, variables)
        self.assertIn('errors', response.to_dict())

    # Add Volunteer
    def test_add_volunteer(self):
        community = self.create_dummy_community()
        volunteers = community.volunteers.all()
        self.client.authenticate(volunteers[0])
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

        response = self.client.execute(add_volunteer, variables)
        self.assertIn('errors', response.to_dict())

    # Remove Volunteer
    def test_remove_volunteer(self):
        community = self.create_dummy_community()
        volunteers = community.volunteers.all()
        self.client.authenticate(volunteers[0])
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

        response = self.client.execute(remove_volunteer, variables)
        self.assertIn('errors', response.to_dict())

    # Create Event
    def test_create_event(self):
        community = self.create_dummy_community()
        volunteers = community.volunteers.all()
        self.client.authenticate(volunteers[0])
        category = self.create_dummy_category()

        start_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))
        time.sleep(1)
        end_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))

        create_event = '''
        mutation createEvent ($address: String, $category: ID!, $city: String, $community: ID, $country: String, $description: String!, $endTime: DateTime!, $kind: String!, $liveUrl: String, $maxRsvp: Int, $name: String!, $startTime: DateTime!, $tags: [String]) {
            createEvent (address: $address, category: $category, city: $city, community: $community, country: $country, description: $description, endTime: $endTime, kind: $kind, liveUrl: $liveUrl, maxRsvp: $maxRsvp, name: $name, startTime: $startTime, tags: $tags) {
                event {
                    address
                    category {
                        id
                    }
                    community {
                        id
                    }
                    city
                    country
                    description
                    kind
                    liveUrl
                    maxRsvp
                    name
                    tags {
                        name
                    }
                    startTime
                    endTime
                }
            }
        }
        '''

        variables = {
            "address": "Test_address",
            "category": category.id,
            "city": "Test_city",
            "community": community.id,
            "country": "Test_country",
            "description": "Test_description",
            "kind": "V",
            "liveUrl": "https://github.com/arpitvaghela/EveRecon-api",
            "maxRsvp": 50,
            "name": "Test_event",
            "startTime": start_time,
            "endTime": end_time,
            "tags": ["Test_tag1", "Test_tag2", "Test_tag3"]
        }

        response = self.client.execute(create_event, variables)
        self.assertIn('errors', response.to_dict())

    # Update event
    def test_update_event(self):
        event = self.create_dummy_event()
        volunteers = event.community.volunteers.all()
        self.client.authenticate(volunteers[0])

        community = Community.objects.get(id=event.community.id)
        category = Category.objects.get(id=event.category.id)

        start_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))
        time.sleep(1)
        end_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))

        update_event = '''
        mutation updateEvent ($address: String, $category: ID, $city: String, $country: String, $description: String, $endTime: DateTime, $id: ID!, $kind: String, $liveUrl: String, $maxRsvp: Int, $name: String, $startTime: DateTime, $tags: [String]) {
            updateEvent (address: $address, category: $category, city: $city, country: $country, description: $description, endTime: $endTime, id: $id, kind: $kind, liveUrl: $liveUrl, maxRsvp: $maxRsvp, name: $name, startTime: $startTime, tags: $tags) {
                event {
                    address
                    category {
                        id
                    }
                    community {
                        id
                    }
                    city
                    country
                    description
                    kind
                    liveUrl
                    maxRsvp
                    name
                    tags {
                        name
                    }
                    startTime
                    endTime
                }
            }
        }
        '''

        variables = {
            "address": "Test_address",
            "category": category.id,
            "city": "Test_city",
            "community": community.id,
            "country": "Test_country",
            "description": "Test_description",
            "kind": "V",
            "liveUrl": "https://github.com/arpitvaghela/EveRecon-api/tree/backend",
            "maxRsvp": 50,
            "id": event.id,
            "name": "Test_event",
            "tags": ["Test_tag1", "Test_tag2", "Test_tag3"],
            "startTime": start_time,
            "endTime": end_time,
        }

        response = self.client.execute(update_event, variables)
        self.assertIn('errors', response.to_dict())

    # Delete Event
    def test_delete_event(self):
        event = self.create_dummy_event()
        volunteers = event.community.volunteers.all()
        self.client.authenticate(volunteers[0])

        delete_event = '''
            mutation deleteEvent ($id: ID) {
            deleteEvent (id: $id) {
                ok
            }
        }
        '''

        variables = {
            "id": event.id
        }

        response = self.client.execute(delete_event, variables)
        self.assertIn('errors', response.to_dict())

    # Create Community testing
    def test_create_community(self):
        community = self.create_dummy_community()
        volunteers = community.volunteers.all()
        self.client.authenticate(volunteers[0])

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
                    leader
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

        response = self.client.execute(create_community, variables)
        self.assertIn('errors', response.to_dict())

    # Delete Community
    def test_delete_community(self):
        community = self.create_dummy_community()
        volunteers = community.volunteers.all()
        self.client.authenticate(volunteers[0])

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

        response = self.client.execute(delete_community, variables)
        self.assertIn('errors', response.to_dict())

    # Add CoreMember
    def test_add_core_member(self):
        community = self.create_dummy_community()
        volunteers = community.volunteers.all()
        self.client.authenticate(volunteers[0])

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

        response = self.client.execute(add_core_member, variables)
        self.assertIn('errors', response.to_dict())

    # Remove CoreMember
    def test_remove_core_member(self):
        community = self.create_dummy_community()
        volunteers = community.volunteers.all()
        self.client.authenticate(volunteers[0])

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

        response = self.client.execute(remove_core_member, variables)
        self.assertIn('errors', response.to_dict())

    # Add Speaker
    def test_add_speaker(self):
        event = self.create_dummy_event()
        volunteers = event.community.volunteers.all()
        self.client.authenticate(volunteers[0])
        speaker = self.create_dummy_speaker()

        add_speaker = '''
            mutation addSpeaker ($eventid: ID!, $speakerid: ID!) {
                addSpeaker (eventid: $eventid, speakerid: $speakerid) {
                    ok
                }
            }
            '''

        variables = {
            "eventid": event.id,
            "speakerid": speaker.id
        }

        response = self.client.execute(add_speaker, variables)
        self.assertIn('errors', response.to_dict())

    # Remove Speaker
    def test_remove_speaker(self):
        event = self.create_dummy_event()
        volunteers = event.community.volunteers.all()
        self.client.authenticate(volunteers[0])
        speaker = self.create_dummy_speaker()

        remove_speaker = '''
            mutation removeSpeaker ($eventid: ID!, $speakerid: ID!) {
                removeSpeaker (eventid: $eventid, speakerid: $speakerid) {
                    ok
                }
            }
            '''

        variables = {
            "eventid": event.id,
            "speakerid": speaker.id
        }

        data = {"ok": True}
        response = self.client.execute(remove_speaker, variables)
        self.assertIn('errors', response.to_dict())

    # check-in event
    def test_checkin_event(self):
        event = self.create_dummy_event()
        user = self.create_dummy_user()
        self.client.authenticate(user)

        register = '''
        mutation registerEvent ($id: ID!) {
            registerEvent (id: $id) {
                event{
                    id
                }
            }
        }
        '''
        variables_register = {
            'id': event.id
        }
        output = self.client.execute(register, variables_register)

        volunteers = event.community.volunteers.all()
        self.client.authenticate(volunteers[0])

        # check-in
        checkin_event = '''
            mutation checkinEvent ($eventid: ID!, $userid: ID!) {
                checkinEvent (eventid: $eventid, userid: $userid) {
                    ok
                    message
                }
            }
        '''

        variables_check_in = {
            'eventid': event.id,
            'userid': user.id
        }

        data_check_in = {'ok': True, 'message': 'Successfully Checkedin'}

        response_check_in = self.client.execute(checkin_event, variables_check_in)
        self.assertNotIn('errors', response_check_in.to_dict())
        content_check_in = list(response_check_in.data.items())[0][1]
        self.assertEquals(content_check_in, data_check_in)

        # uncheck-in
        uncheckin_event = '''
        mutation uncheckinEvent ($eventid: ID!, $userid: String!) {
            uncheckinEvent (eventid: $eventid, userid: $userid) {
                ok
                message
            }
        }
        '''
        variables_uncheck_in = {
            'eventid': event.id,
            'userid': user.id
        }
        data_uncheck_in = {'ok': True, 'message': 'Checkin removed'}

        response_uncheck_in = self.client.execute(uncheckin_event, variables_uncheck_in)
        self.assertNotIn('errors', response_uncheck_in.to_dict())
        content_uncheck_in = list(response_uncheck_in.data.items())[0][1]
        self.assertEquals(content_uncheck_in, data_uncheck_in)

    # View Event RSVP
    def test_view_event_RSVP(self):
        event = self.create_dummy_event()
        volunteers = event.community.volunteers.all()
        self.client.authenticate(volunteers[0])

        users = []
        for i in range(0, 5):
            user = self.create_dummy_user()
            self.client.authenticate(user)
            register_event = '''
                mutation registerEvent ($id: ID!) {
                    registerEvent (id: $id) {
                        event {
                            id
                        }
                    }
                }
                '''
            variables = {
                'id': event.id
            }
            self.client.execute(register_event, variables)
            users.append({'id': str(user.id), 'username': user.username, 'email': user.email})

        event_RSVP = '''
            query eventById ($id: ID) {
                eventById (id: $id) {
                    attendees {
                        id
                        username
                        email
                    }
                }
            }
            '''
        var = {
            'id': event.id
        }

        data = {
            'attendees': users
        }

        response = self.client.execute(event_RSVP, var)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)