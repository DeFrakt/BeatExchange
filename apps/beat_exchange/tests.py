from django.test import TestCase, Client
from models import *

class BeatExchangeTest(TestCase):
    #test urls
    def test_urls(self):
        #simulate request
        client = Client()
     
        self.assertEqual(client.get('/').status_code, 200)

    #test models
    def test_model_beat(self):
        beat = Beat.objects.create(name = "Pink Floyd")
        self.assertEqual(beat.name, "Pink Floyd")

    def test_view_create(self):
        c = Client()
        c.post('/')

    