from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        '''Stuff to do before every test.'''
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        '''testing loading homepage with gameboard'''
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Play Boggle!</h1>", html)

    def test_vaild_word(self):
        ''' Test if word is vaild '''
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_word_not_board(self):
        ''' test if word is in the dictionary'''

        self.client.get("/")
        response = self.client.get("/check-word?word=impossible")
        self.assertEqual(response.json['result'], 'not-on-board')
        