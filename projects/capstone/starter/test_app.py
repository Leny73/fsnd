import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Location, Event


class CapstoneTestCases(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('lyuben', 'temp123!','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_event = {
            'name': 'Test_event',
            'location': 'test_location',
        }

        self.new_locations = {
            'name': 'Test_location',
            'location': 'test_location'
        }

        self.Location_Manager_jwt = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjdJbkN0bnQwUjg4Rll6ZnlIbWtsZCJ9.eyJpc3MiOiJodHRwczovL3R3Ym0uZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE2MDIyNTQ0NTkzMjM0MzQ0MDU0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MjE2OTcxNzgsImV4cCI6MTYyMTcwNDM3OCwiYXpwIjoiYUd1MGhjRTUzbjRWMFlMRW43Y0lHOFBBczBkQkppaXkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpsb2NhdGlvbnMiLCJwb3N0OmxvY2F0aW9ucyJdfQ.JOqKqY4dM8elTeECOTvCj1XPqNZuwBRRdFu8RekJWeI0zur9gIC6JJ0nNFHHGm7NYrJpW0orqEt0LGi5DcCoRLg6xz5r3-BQPkdXbB_LP1iXx4ZnS-ovpAuj0KUnSeMgvkRYfR1aEzU6ZN9HsA3dkgaRGmxHAhb4E-KJII-Ue-T_mOzjejm6By_NDi47IkZ0XrmizkRdsi8Gwxb6oboVAl98UqrkLZX9m7dS3XfEdy61gJPOV8Kfwu1vOstslvE5TmwvFDzcm_4lzje_eimCB_uTJ8b5mOp0J1Qksd0ajxxHD__mwxDzuzsDrhbU63FTEsUJOrZQ6QyH6GplpH3H8A'
        self.Event_Manager_jwt = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjdJbkN0bnQwUjg4Rll6ZnlIbWtsZCJ9.eyJpc3MiOiJodHRwczovL3R3Ym0uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwYTkxNjE2YTdlYmM5MDA2YTRjY2UyZiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjIxNjk3MzYzLCJleHAiOjE2MjE3MDQ1NjMsImF6cCI6ImFHdTBoY0U1M240VjBZTEVuN2NJRzhQQXMwZEJKaWl5Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZXZlbnRzIiwiZ2V0OmV2ZW50cyIsInBhdGNoOmV2ZW50cyIsInBvc3Q6ZXZlbnRzIl19.ATXy8HUugwcfmJCr1ei7SBs4_ccRrOho_GRc6NyfONXeURKrHADMhlJN7-d1CUqKG8qIgKRjdEhWfLy2oEcJflu0-C1zMccw0OeSF3etuzDh1MeptdL_ae2gPKnkIYih8A_8iWF-4wOOFMdQHYW6SPSZyWz3BynOtYyhNty1G4zGov13IzEriXuTJwzUiD_bqInfbFz1N-A5vJGaRMayF0Zx6Ilu3n41aIHxhb5EbarNwSAps10LAMoCYEb4XQJ_9PQmRqsOUwDMFPG1ti4rpVVGqOufeVnNq9DDMXB7JU8UT3vMtMC6iSe8hIqNqYs0qY2YCPst5NfLY-f4HxawjQ'
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass



    
    
    def test_get_locations(self):
        Locations_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Location_Manager_jwt 
        }
        res = self.client().get('/locations', headers=Locations_Manager_jwt)
        print(res.data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_locations'])
        self.assertTrue(len(data['locations']))

    def test_create_location(self):
        Locations_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Location_Manager_jwt 
        }
        res = self.client().post('/locations', headers=Locations_Manager_jwt, json=self.new_locations)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_location_authorize_fail(self):
        res = self.client().post('/locations')
        self.assertEqual(res.status_code, 401)

    def test_get_locations_authorize_fail(self):
        res = self.client().get('/locations')
        self.assertEqual(res.status_code, 401)

    def test_get_events_by_locations_manager(self):
        Locations_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Location_Manager_jwt 
        }
        res = self.client().get('/events', headers=Locations_Manager_jwt)
        self.assertEqual(res.status_code, 401)

    def test_post_events_by_locations_manager(self):
        Locations_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Location_Manager_jwt 
        }
        res = self.client().post('/events', headers=Locations_Manager_jwt, json=self.new_event)
        self.assertEqual(res.status_code, 401)

    def test_patch_events_by_locations_manager(self):
        Locations_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Location_Manager_jwt 
        }
        res = self.client().patch('/events/1', headers=Locations_Manager_jwt)
        self.assertEqual(res.status_code, 401)

    def test_delete_events_by_locations_manager(self):
        Locations_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Location_Manager_jwt 
        }
        res = self.client().delete('/events/2', headers=Locations_Manager_jwt)
        self.assertEqual(res.status_code, 401)

    def test_get_events(self):
        Event_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Event_Manager_jwt
        }
        res = self.client().get('/events', headers=Event_Manager_jwt)
        print(res.data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_events'])
        self.assertTrue(len(data['events']))
        self.assertTrue(data['data'])

    def test_create_event(self):
        Event_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Event_Manager_jwt
        }
        res = self.client().post('/events', headers=Event_Manager_jwt, json=self.new_event)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_event_authorize_fail(self):
        res = self.client().post('/events')
        self.assertEqual(res.status_code, 401)

    def test_get_events_authorize_fail(self):
        res = self.client().get('/events')
        self.assertEqual(res.status_code, 401)

    def test_patch_event(self):
        Event_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Event_Manager_jwt
        }
        res = self.client().patch('/events/4', headers=Event_Manager_jwt, json=self.new_event)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)   

    def test_delete_event(self):
        Event_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Event_Manager_jwt
        }
        res = self.client().delete('/events/2', headers=Event_Manager_jwt)
        self.assertEqual(res.status_code, 200)

    def test_get_locations_by_event_manager(self):
        Event_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Event_Manager_jwt
        }
        res = self.client().get('/locations', headers=Event_Manager_jwt)
        self.assertEqual(res.status_code, 401)

    def test_post_events_by_locations_manager(self):
        Event_Manager_jwt = {
            'Content-Type': 'application/json',
            'Authorization': self.Event_Manager_jwt
        }
        res = self.client().post('/locations', headers=Event_Manager_jwt)
        self.assertEqual(res.status_code, 401)

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
