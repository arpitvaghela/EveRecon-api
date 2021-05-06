import time
import pytz
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
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

    # Create Event
    def test_create_event(self):
        community = self.create_dummy_community()
        leader = community.leader
        self.client.authenticate(leader)
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

        tags = []
        for i in (variables['tags']):
            tags.append({"name": i.lower()})

        data = {"event": {
            "address": variables['address'],
            "category": {
                "id": str(variables['category'])
            },
            "community": {
                "id": str(variables['community'])
            },
            "city": variables['city'],
            "country": variables['country'],
            "description": variables['description'],
            "kind": "V",
            "liveUrl": variables['liveUrl'],
            "maxRsvp": variables['maxRsvp'],
            "name": variables['name'],
            "startTime": variables['startTime'],
            "endTime": variables['endTime'],
            "tags": tags
        }}

        response = self.client.execute(create_event, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        content['event']['startTime'] = dateparse.parse_datetime(content['event']["startTime"])
        content['event']['endTime'] = dateparse.parse_datetime(content['event']["endTime"])
        self.assertEquals(content, data)

    # Update event
    def test_update_event(self):
        event = self.create_dummy_event()
        leader = event.community.leader
        self.client.authenticate(leader)
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

        tags = []
        for i in (variables['tags']):
            tags.append({"name": i.lower()})

        data = {"event": {
            "address": variables['address'],
            "category": {
                "id": str(variables['category'])
            },
            "community": {
                "id": str(variables['community'])
            },
            "city": variables['city'],
            "country": variables['country'],
            "description": variables['description'],
            "kind": "V",
            "liveUrl": variables['liveUrl'],
            "maxRsvp": variables['maxRsvp'],
            "name": variables['name'],
            "tags": tags,
            "startTime": variables['startTime'],
            "endTime": variables['endTime'],
        }}

        response = self.client.execute(update_event, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        content['event']['startTime'] = dateparse.parse_datetime(content['event']["startTime"])
        content['event']['endTime'] = dateparse.parse_datetime(content['event']["endTime"])
        self.assertEquals(content, data)

    # Delete Event
    def test_delete_event(self):
        event = self.create_dummy_event()
        leader = event.community.leader
        self.client.authenticate(leader)

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

        data = {"ok": True}

        response = self.client.execute(delete_event, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Register Event
    def test_register_event(self):
        event = self.create_dummy_event()
        user = self.create_dummy_user()
        self.client.authenticate(user)

        register_event = '''
        mutation registerEvent ($id: ID!) {
            registerEvent (id: $id) {
                event {
                    id
                    name
                    community {
                        id
                        name
                        description
                    } 
                }
            }
        }
        '''

        variables = {
            "id": event.id
        }

        data = {'event': {
            'id': str(event.id),
            'name': event.name,
            'community': {
                'id': str(event.community.id),
                'name': event.community.name,
                'description': event.community.description
            }
        }}

        response = self.client.execute(register_event, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # EventByID testing
    def test_event_by_id(self):
        event = self.create_dummy_event()
        leader = event.community.leader
        self.client.authenticate(leader)

        event_by_id = '''
            query eventById ($id: ID){
                 eventById(id: $id) {
                     name
                 }
             }
        '''

        variables = {
            'id': event.id
        }

        data = {
            "name": event.name
        }

        response = self.client.execute(event_by_id, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Create Speaker
    def test_create_speaker(self):
        create_speaker = '''
            mutation createSpeaker ($description: String, $email: String, $facebook: String, $firstName: String!, $instagram: String, $lastName: String) {
                createSpeaker (description: $description, email: $email, facebook: $facebook, firstName: $firstName, instagram: $instagram, lastName: $lastName) {
                    speaker {
                        description
                        email
                        facebook
                        instagram
                        firstName
                        lastName
                    }
                }
            }
            '''

        variables = {
            "description": "Test_Description",
            "email": "test@gmail.com",
            "facebook": "https://www.facebook.com/mrparth23/",
            "firstName": "Test_firstname",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "lastName": "Test_lastname"
        }

        data = {"speaker": {
            "description": variables['description'],
            "email": variables['email'],
            "facebook": variables['facebook'],
            "instagram": variables['instagram'],
            "firstName": variables['firstName'],
            "lastName": variables['lastName']
        }}

        response = self.client.execute(create_speaker, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Add Speaker
    def test_add_speaker(self):
        event = self.create_dummy_event()
        leader = event.community.leader
        self.client.authenticate(leader)
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

        data = {"ok": True}
        response = self.client.execute(add_speaker, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Remove Speaker
    def test_remove_speaker(self):
        event = self.create_dummy_event()
        leader = event.community.leader
        self.client.authenticate(leader)
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
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Speaker by email
    def test_speaker_by_email(self):
        speaker = self.create_dummy_speaker()

        speaker_by_email = '''
            query speakerByEmail ($email: String) {
                speakerByEmail (email: $email) {
                    firstName
                    lastName
                    email
                }
            }

        '''

        variables = {
            'email': speaker.email
        }

        data = {
            'firstName': speaker.first_name,
            'lastName': speaker.last_name,
            'email': variables['email']
        }

        response = self.client.execute(speaker_by_email, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # All speaker
    def test_all_speaker(self):

        speaker = []
        for i in range(0, 5):
            speak = self.create_dummy_speaker()
            speaker.append({'firstName': speak.first_name, 'lastName': speak.last_name, 'email': speak.email})

        all_speaker = '''
            query allSpeaker {
                allSpeaker {
                    firstName
                    lastName
                    email
                }
            }
        '''

        data = speaker
        response = self.client.execute(all_speaker)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # All category
    def test_all_category(self):
        category = []
        for i in range(0, 5):
            cat = self.create_dummy_category()
            category.append({'id': str(cat.id), 'name': cat.name})

        all_category = '''
        query categories{
            categories{
                id
                name
            }
        }
        '''
        data = category
        response = self.client.execute(all_category)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Events of community
    def test_events_of_community(self):
        event = self.create_dummy_event()

        events_of_community = '''
        query communityById ($id: ID) {
            communityById (id: $id) {
                id
                name
                description
                email
                events {
                    id
                    name
                    description
                }
            }
        }
        '''
        variables = {
            "id": event.community.id
        }

        data = {
            'id': str(event.community.id),
            'name': event.community.name,
            'description': event.community.description,
            'email': event.community.email,
            'events': [{'id': str(event.id), 'name': event.name, 'description': event.description}]
        }
        response = self.client.execute(events_of_community, variables)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

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

        leader = event.community.leader
        self.client.authenticate(leader)

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
        leader = event.community.leader
        self.client.authenticate(leader)

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

    # My Registered Event
    def test_my_event(self):
        myprofile = self.create_dummy_user()
        self.client.authenticate(myprofile)
        event = []
        eve = self.create_dummy_event()
        event.append({'id': str(eve.id), 'name': eve.name, 'description': eve.description})

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
            'id': eve.id
        }

        self.client.execute(register_event, variables)

        event_registered = '''
            query myprofile {
                myprofile {
                    eventsAttended {
                        id
                        name
                        description
                    }
                }
            }
            '''
        data = {
            'eventsAttended': event
        }

        response = self.client.execute(event_registered)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.client.execute(event_registered, data)

    # Event time validation test in createEvent
    def test_create_event_time_validation(self):
        community = self.create_dummy_community()
        category = self.create_dummy_category()

        start_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))
        time.sleep(2)
        end_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))

        create_event_time = '''
            mutation createEvent ($address: String, $category: ID!, $city: String, $community: ID, $country: String, $description: String!, $endTime: DateTime!, $kind: String!, $liveUrl: String, $maxRsvp: Int, $name: String!, $startTime: DateTime!, $tags: [String]) {
                createEvent (address: $address, category: $category, city: $city, community: $community, country: $country, description: $description, endTime: $endTime, kind: $kind, liveUrl: $liveUrl, maxRsvp: $maxRsvp, name: $name, startTime: $startTime, tags: $tags) {
                    event {
                        name
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
            "startTime": end_time,
            "endTime": start_time,
            "tags": ["Test_tag1", "Test_tag2", "Test_tag3"]
        }

        response = self.client.execute(create_event_time, variables)
        self.assertIn('errors', response.to_dict())

    # Facebook validation test in createSpeaker
    def test_create_speaker_facebook_validation(self):
        create_speaker_facebook = '''
            mutation createSpeaker ($description: String, $email: String, $facebook: String, $firstName: String!, $instagram: String, $lastName: String) {
                createSpeaker (description: $description, email: $email, facebook: $facebook, firstName: $firstName, instagram: $instagram, lastName: $lastName) {
                    speaker {
                        facebook
                    }
                }
            }
            '''

        variables = {
            "description": "Test_Description",
            "email": "test@gmail.com",
            "facebook": "https://www.facebk.com/mrparth23/",
            "firstName": "Test_firstname",
            "instagram": "https://www.instagram.com/mr.parth23/",
            "lastName": "Test_lastname"
        }

        response = self.client.execute(create_speaker_facebook, variables)
        self.assertIn('errors', response.to_dict())

    # Instagram validation test in createSpeaker
    def test_create_speaker_instagram_validation(self):
        create_speaker_instagram = '''
            mutation createSpeaker ($description: String, $email: String, $facebook: String, $firstName: String!, $instagram: String, $lastName: String) {
                createSpeaker (description: $description, email: $email, facebook: $facebook, firstName: $firstName, instagram: $instagram, lastName: $lastName) {
                    speaker {
                        instagram
                    }
                }
            }
            '''

        variables = {
            "description": "Test_Description",
            "email": "test@gmail.com",
            "facebook": "https://www.facebook.com/mrparth23/",
            "firstName": "Test_firstname",
            "instagram": "https://www.instam.com/mr.parth23/",
            "lastName": "Test_lastname"
        }
        response = self.client.execute(create_speaker_instagram, variables)
        self.assertIn('errors', response.to_dict())

    # Max Event RSVP
    def test_max_event_RSVP_validation(self):
        try:
            with transaction.atomic():
                event = self.create_dummy_event()
                event.max_RSVP = 0
                event.save()

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

                leader = event.community.leader
                self.client.authenticate(leader)

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

                response = self.client.execute(event_RSVP, variables)
                self.assertIn('errors', response.to_dict())

        except IntegrityError:
            pass

    # test leader, core-members and volunteers auto registration
    def test_auto_registration_validation(self):
        community = self.create_dummy_community()
        leader = community.leader
        self.client.authenticate(leader)
        category = self.create_dummy_category()

        start_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))
        time.sleep(1)
        end_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))

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
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]

        event_attendees = '''
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

        event = Event.objects.get(id=int(content['event']['id']))
        var = {'id': event.id}

        users = []
        leader = event.community.leader
        users.append({'id': str(leader.id), 'username': leader.username, 'email': leader.email})

        for user in event.community.core_members.all():
            js = {'id': str(user.id), 'username': user.username, 'email': user.email}
            users.append(js)

        for user in event.community.volunteers.all():
            js = {'id': str(user.id), 'username': user.username, 'email': user.email}
            users.append(js)

        data = {'attendees': users}
        response = self.client.execute(event_attendees, var)
        self.assertNotIn('errors', response.to_dict())
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)