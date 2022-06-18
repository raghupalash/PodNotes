from django.db import models

# Create your models here.
class User(models.Model):
    user_spotify_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.username}"

class Entry(models.Model):
    podcast_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.podcast_id} of {self.user.username}"

class Note(models.Model):
    time = models.CharField(max_length=20)
    text = models.TextField()
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.time} - {self.text}"