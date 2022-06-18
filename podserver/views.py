import os
from telnetlib import STATUS
import uuid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .utils import session_cache_path
from .credentials import client_id, client_secret

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

    return render(request, "podserver/app.html")

def search(request, query):
    # Check if logged in
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
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
            pos = spotify.current_playback()

            spotify.seek_track(pos["progress_ms"] + 15000)
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


    
