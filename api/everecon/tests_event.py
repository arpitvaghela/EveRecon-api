from django.utils import dateparse
from django.utils import timezone
from datetime import datetime
from .models import *
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import pytz
import warnings

# warnings.filterwarnings("ignore")

GraphQLTestCase.GRAPHQL_URL = "http://127.0.0.1:8000/graphql/"
print(GraphQLTestCase.GRAPHQL_URL)

global id
id = 1


class EveReconTest(JSONWebTokenTestCase):

    def create_dummy_user(self):
        global id
        user = User.objects.create(
            username="Test_username_" + str(id),
            password = "Test@10",
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
        # date_time = datetime.now()
        date_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))
        event = Event.objects.create(
            name="Test_event",
            address="Test_address",
            category=category,
            city="Test_city",
            community=community,
            country="Test_country",
            description="Test_description",
            end_time=date_time,
            kind="V",
            live_URL="https://github.com/arpitvaghela/EveRecon-api",
            max_RSVP=50,
            start_time=date_time
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
        return Category.objects.create(name="Test_category")

    def setUp(self):
        self.user = get_user_model().objects.create(username='test',password="Test@10")
        self.client.authenticate(self.user)

    # Create Event
    def test_create_event(self):
        community = self.create_dummy_community()
        category = self.create_dummy_category()

        # date_time = timezone.now()
        date_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))

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
            "startTime": date_time,
            "endTime": date_time,
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
        content = list(response.data.items())[0][1]
        content['event']['startTime'] = dateparse.parse_datetime(content['event']["startTime"])
        content['event']['endTime'] = dateparse.parse_datetime(content['event']["endTime"])
        self.assertEquals(content, data)

    # Update event
    def test_update_event(self):
        event = self.create_dummy_event()
        community = Community.objects.get(id=event.community.id)
        category = Category.objects.get(id=event.category.id)

        # date_time = timezone.now()
        date_time = timezone.localtime(timezone.now(), pytz.timezone('Asia/Kolkata'))

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
            "startTime": date_time,
            "endTime": date_time,
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
        content = list(response.data.items())[0][1]
        content['event']['startTime'] = dateparse.parse_datetime(content['event']["startTime"])
        content['event']['endTime'] = dateparse.parse_datetime(content['event']["endTime"])
        self.assertEquals(content, data)

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

        variables = {
            "id": event.id
        }

        data = {"ok": True}

        response = self.client.execute(delete_event, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # Register Event
    def test_register_event(self):
        event = self.create_dummy_event()

        register_event = '''
        mutation registerEvent ($id: ID!) {
            registerEvent (id: $id) {
                event {
                    name
                }  
            }
        }
        '''

        variables = {
            "id": event.id
        }

        data = {"event": {
            "name": event.name
        }}

        response = self.client.execute(register_event, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # EventByID testing
    def test_event_by_id(self):
        event = self.create_dummy_event()
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
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

    # All events
    def test_events(self):
        events = []
        for i in range(0, 3):
            event = self.create_dummy_event()
            js = {"name": event.name, "description": event.description, "kind": event.kind,
                  "address": event.address, "category": {"id": str(event.category.id)}}
            events.append(js)

        all_events = '''
            query events {
                events {
                    name
                    description
                    kind
                    address
                    category {
                        id
                    }                        
                }
            }
        '''

        data = events

        response = self.client.execute(all_events)
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
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

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

        variables = {
            "eventid": event.id,
            "speakerid": speaker.id
        }

        data = {"ok": True}
        response = self.client.execute(add_speaker, variables)
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)

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

        variables = {
            "eventid": event.id,
            "speakerid": speaker.id
        }

        data = {"ok": True}
        response = self.client.execute(remove_speaker, variables)
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
        content = list(response.data.items())[0][1]
        self.assertEquals(content, data)