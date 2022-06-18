from django.test import Client, TestCase
import uuid

from .models import Entry, Note, User

# Create your tests here.
class NoteTestCase(TestCase):
    def setup(self):
        client = Client()
        user = User(user_spotify_id="5ai9kmle7y2354tztz7pnlsfq", username="raghu_palash")
        user.save()


    def test_post_note(self):
        data = dict(time="31236", text="hello world")

        session = self.client.session
        session["uuid"] = str(uuid.uuid4())
        session.save()
        
        print(Entry.objects.all())
        print(Note.objects.all())
        x = self.client.post("/addNote", data=data, follow=True)
        print(x)
        self.assertEqual(x.status_code, 200)