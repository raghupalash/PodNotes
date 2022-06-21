# API Documentation

## Note Creation and Saving.

`/currentPos` - **GET**

Get the current position of the current playing track in milliseconds.

`/addNote` - **POST**

Data - A JSON object with two keys and their respective values:

- `time` - Time in milliseconds.
- `text` - Text that user inputed.

Headers would need to contain a CSRF cookie, it's not a priority to have it right now, so I think I might bypass it as of now.


## Media Player controls.

`/media/<action>` - **PUT**

No Data required, the query you give along with the url is data.

action should be one of these - 

- pause
- play
- skip15 - To skip ahead 15 seconds.

Depending on the action chosen, the Spotify player on the Spotify app will play, pause or skip forwards by 15 seconds.


## Search

`/search?query=<user_query>` - **GET**

user_query will be the string inputed by the user.

**Return**:

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

