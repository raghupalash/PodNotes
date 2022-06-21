import os
from telnetlib import STATUS
import uuid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .utils import session_cache_path
from .credentials import client_id, client_secret

from .models import Entry, Note, User

# Test imports
from django.test import Client
import pprint

os.environ["SPOTIPY_CLIENT_ID"] = client_id
os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:8000/"


SCOPE = "user-library-read user-modify-playback-state user-read-playback-state user-read-currently-playing"

# Create your views here.
def index(request):
    if not request.session.get("uuid"):
        # Step 1. Visitor is unknown, give random ID
        request.session["uuid"] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope=SCOPE,
        cache_handler=cache_handler, 
        show_dialog=True
    )
    
    # 3 then 2, the order is necessary
    if request.GET.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.GET.get("code"))
        return redirect("/")

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render(request, "podserver/landing_page.html", {
            "auth_url": auth_url
        })

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    
    current_user = spotify.current_user()
    user = User.objects.filter(user_spotify_id=current_user["id"])
    if not len(user):
        user = User(user_spotify_id=current_user["id"], username=current_user["display_name"])
        user.save()
    return render(request, "podserver/app.html")

def search(request):
    # Check if logged in
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    query = request.GET["query"]
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    search_res = spotify.search(query, limit=1, offset=0, type="show,episode")
    return JsonResponse(search_res)

def media(request, query):
    # Check if logged in
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    if query not in ["pause", "play", "skip15"]:
        return HttpResponse("Wrong query, use 'pause', 'play' or 'skip15'", status=400)
    
    try:
        if query == "pause":
            spotify.pause_playback()
        elif query == "play":
            spotify.start_playback()
        else:
            current = spotify.current_playback(additional_types="episode")
            spotify.seek_track(current["progress_ms"] + 15000)
    except:
        return HttpResponse("An unknown error occured", status=400)

    return HttpResponse("ok")

def currentPos(request):
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    try:
        pos = spotify.current_playback()["progress_ms"]
    except:
        return HttpResponse("An unkown error occured", status=500)

    return JsonResponse({"currentPos": pos})

def addNote(request):
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    if request.method == "POST":
        if not request.POST.get("time") or not request.POST.get("text"):
            return HttpResponse("Time or Note not provided.", status=400)
        
        time = str(request.POST["time"])
        text = str(request.POST["text"])

        user = User.objects.get(user_spotify_id=spotify.current_user()["id"])

        # Get the current playing podcast info
        podcast = spotify.current_playback(additional_types="episode")
        if podcast["item"]["type"] == "track":
            return HttpResponse("You are not listening to a podcast, are you?", status=400)

        # Search db for that podcast and user id
        entry = Entry.objects.filter(podcast_id=podcast["item"]["id"], user=user)
        if len(entry) == 0:
            entry = Entry(podcast_id=podcast["item"]["id"], user=user)
            entry.save()

        # if not present then create an entry, add it to user and then make note
        note = Note(time=time, text=text, entry=entry)
        note.save()
        
        return HttpResponse("ok")

def entry(request):
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    user_id = spotify.current_user()["id"]
    entries = Entry.objects.filter(user__user_spotify_id=user_id)
    if not len(entries):
        return HttpResponse("No entries found.", status=404)
    episode_ids = [entry.podcast_id for entry in entries]
    episodes = spotify.episodes(episode_ids)

    return JsonResponse(episodes)


def testNote(request):
    c = Client()
    session = c.session
    session["uuid"] = "5d61cf46-6f53-44c8-9e81-467e54320f01"
    session.save()
    data = dict(time="123455", text="hellow world!")
    res = c.post("/addNote", data=data)
    return HttpResponse(res)


    
