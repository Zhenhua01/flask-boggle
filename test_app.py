from unittest import TestCase
from urllib import response

from flask import current_app

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<!-- testing template -->', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            
            resp = client.post('/api/new-game')
            current_game = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertIs(type(current_game), dict)
            self.assertIs(type(current_game['game_id']), str)
            self.assertIs(type(current_game['board']), str)
    
    def test_check_for_legal_word(self):
        """Test checking for a legal word"""

        with self.client as client:
            
            resp = client.post('/api/new-game')
            current_game = resp.get_json()
            breakpoint()
            lw_response = client.post('/api/score-word',
                json = {'game_id':f"{current_game['game_id']}",'word':'ear'})
            json_lw_response = lw_response.get_json()
            breakpoint()

           
