## Installation
To install all the python requirements of this project:

```
pip install requirements.txt
```
To run the server:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Update Frontend
The Django server loads the index.html template in the build folder. So having a build folder is necessary.
```
cd frontend
npm run build
cd ..
python manage.py runserver
```

## API Documentation

### Note Creation and Saving.

`/currentPos` - **GET**

Get the current position of the current playing track in milliseconds.

`/addNote` - **POST**

Data - A JSON object with two keys and their respective values:

- `time` - Time in milliseconds.
- `text` - Text that user inputed.

Headers would need to contain a CSRF cookie, it's not a priority to have it right now, so I think I might bypass it as of now.


### Media Player controls.

`/media/<action>` - **PUT**

No Data required, the query you give along with the url is data.

action should be one of these - 

- pause
- play
- skip15 - To skip ahead 15 seconds.

Depending on the action chosen, the Spotify player on the Spotify app will play, pause or skip forwards by 15 seconds.

**Note** - In case of action = play, you can provide also provide a query:
`/media/play?uri=`


### Search

`/search?query=<user_query>` - **GET**

user_query will be the string inputed by the user.

**Response**:

A json object will be returned with following hierarchy -

- episodes
   - items (an array of objects, where each object is:)
       - id
       - images (array containing image objects - height, width, url - first item is best quality)
       - name
       - description
       - uri
- shows
   - items (an array of objects, where each object is:)
       - id
       - images
       - name
       - images
       - description
       - uri

**Note** - Search results should be displayed as hyperlinks where each result
is a hyperlink pointing to `.../media/play?uri={uri}`.

### Entries

`/entries` - GET.

Purpose: To show users the podcasts they made some notes on.

**Response** -

- episodes: array of objects (where each object contains):
    - description
    - id
    - images (array of objects)
       - url
       - height
       - width
   - name

### Notes

`/notes` - GET.

Purpose: Called when user is at the podcast view, i.e., the screen that comes after they clicked on an podcast/entry.
The podcast starts playing, which the user can stop, and below should appear a list of their notes.

**Response** -

- an array of objects like -
    "time": "text"
