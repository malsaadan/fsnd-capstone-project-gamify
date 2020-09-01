# API Reference

## Getting Started

**Base Url:** This app is hosted at `https://fsnd-gamify.herokuapp.com/`, or you could run it locally which is hosted at the default, `https://127.0.0.1:5000/`.

**Authentication:** This app uses Auth0 authentication.
*Auth0 Link: https://gamify-fsnd.us.auth0.com/authorize?audience=gamify&response_type=token&client_id=5xDwhLNUXk0SmdxZGSWcq81iVaANk3mn&redirect_uri=https://fsnd-gamify.herokuapp.com/callback*

## Error Handling

Errors are returned as JSON objects in the following format:

```JSON
{
    "success": false,
    "error": 400,
    "message": "Bad Request"
}
```

The API will return five types of error when requests fail:

| Status Code    | Message      | Description  |
| :------------- | :----------: | -----------: |
| 400            | Bad Request  | The request cannot be fulfilled due to bad syntax.    |
| 405   | Method Not Allowed | A request was made of a resource using a request method not supported by that resource |
| 404   | Resource Not Found | The requested resource could not be found but may be available again in the future. Subsequent requests by the client are permissible.    |
| 422 | Unprocessable Entity | The request was well-formed but was unable to be followed due to semantic errors.|
| 500 | Internal Server Error | A generic error message, given when no more specific message is suitable.|
| 401 | Authorization header is expected | The request has not been applied because it lacks valid authentication credentials for the target resource.|

## Endpoint Library

### Get `/api/games`

* General

  * Returns a list of game objects

* Sample

  * Request: `curl https://fsnd-gamify.herokuapp.com/api/games`

  * Response:

    ```JSON
    {
        "games":[
            {
                "age_rating":"+16",
                "category_id":3,
                "developer_id":2,
                "id":2,
                "image_link":"https://upload.wikimedia.org/wikipedia/en/5/51/Overwatch_cover_art.jpg",
                "name":"overwatch"
            },
            {
                "age_rating":"+18",
                "category_id":3,
                "developer_id":3,
                "id":3,
                "image_link":"https://cdn-products.eneba.com/resized-products/umCbfbG_390x400_1x-0.jpg",
                "name":"call of duty black ops"
            }
        ],
        "success":true,
        "total_games":2
    }
    ```

### Get `/api/games/<game_id>`

* General

  * Returns the details of a game, and a success value.

* Sample

  * Request: `curl -H "Authorization: ${TOKEN}" https://fsnd-gamify.herokuapp.com/api/games/3`

  * Response:

    ```JSON
    {
        "game":{
            "age_rating":"+18",
            "category_id":3,
            "developer_id":4,
            "id":3,
            "image_link":"https://images.goodgam.es/8RomeOKHaf8/enlarge:1/plain/covers/682-valorant-cover.jpg",
            "name":"valorant"
        },
        "success":true
    }
    ```

### DELETE `/api/games/{game_id}`

* General

  * Deletes the game of the given ID if it exists. Returns the ID of the deleted game, success value, and games list.

  * Sample

    * Request: `curl -H "Authorization: ${TOKEN}" -X DELETE https://fsnd-gamify.herokuapp.com/api/games/2`

    * Response:

      ```JSON
      {
        "deleted":2,
        "games":[
            {
                "age_rating":"+18",
                "category_id":3,
                "developer_id":3,
                "id":3,
                "image_link":"https://cdn-products.eneba.com/resized-products/umCbfbG_390x400_1x-0.jpg",
                "name":"call of duty black ops"
            }
        ],
        "success":true
      }
      ```

### POST `/api/games`

* General

  * Creates a new game using the submitted name, age rating, category id, developer id and image link. Returns the newly created game and a success value.
  > Note: In order to add a new game, the associated category and developer must exist first.

  * Sample

    * Request: `curl -H "Content-Type: application/json" -H "Authorization: ${TOKEN}" -d '{"name": "overwatch", "age_rating": "+16", "category_id": 3, "developer_id": 2, "image_link": "https://images-na.ssl-images-amazon.com/images/I/812HBc8O%2BUL._SY445_.jpg"}' -X POST https://fsnd-gamify.herokuapp.com/api/games`

    * Response:

      ```JSON
        {
            "game":{
                "age_rating":"+16",
                "category_id":3,
                "developer_id":2,
                "id":4,
                "image_link":"https://images-na.ssl-images-amazon.com/images/I/812HBc8O%2BUL._SY445_.jpg",
                "name":"overwatch"
            },
            "success":true
        }
      ```

### POST `/api/search?q=<search_term>`

* General

  * Searches for a given text query string and retrieves a list of game objects where the game object's name is a match. Returns number of results, a list of game objects (results), and a success value.

* Sample

  * Request: `curl -X GET https://fsnd-gamify.herokuapp.com/api/search?q=overwatch`

  * Response:

    ```JSON
    {
        "num_results":1,
        "search_results":[
            {
                "age_rating":"+16",
                "category_id":3,
                "developer_id":2,
                "id":4,
                "image_link":"https://images-na.ssl-images-amazon.com/images/I/812HBc8O%2BUL._SY445_.jpg",
                "name":"overwatch"
            }
        ],
        "success":true
    }
    ```

### PATCH `/api/games/<game_id>`

* General

  * Edits the game of the given ID if it exists using the submitted name, age rating, category id, developer id and image link. Returns the ID of the updated game, success value, and games list.
  > Note: the submitted category and developer IDs must exist.

* Sample

  * Request: `curl -H "Content-Type: application/json" -H "Authorization: ${TOKEN}" -d '{"name": "valorant", "age_rating": "+18", "category_id": 3, "developer_id": 4, "image_link": "https://images.goodgam.es/8RomeOKHaf8/enlarge:1/plain/covers/682-valorant-cover.jpg"}' -X PATCH https://fsnd-gamify.herokuapp.com/api/games/3`

  * Response:

    ```JSON
    {
        "games":[
            {
                "age_rating":"+18",
                "category_id":3,
                "developer_id":4,
                "id":3,
                "image_link":"https://images.goodgam.es/8RomeOKHaf8/enlarge:1/plain/covers/682-valorant-cover.jpg",
                "name":"valorant"
            },
            {
                "age_rating":"+16",
                "category_id":3,
                "developer_id":2,
                "id":4,
                "image_link":"https://images-na.ssl-images-amazon.com/images/I/812HBc8O%2BUL._SY445_.jpg",
                "name":"overwatch"
            }
        ],
        "success":true,
        "updated":"3"
    }
    ```

### Get `/api/categories`

* General

  * Returns a list of category objects.

* Sample
  
  * Request: `curl https://fsnd-gamify.herokuapp.com/api/categories`

  * Response:

    ```JSON
    {
        "categories":[
            {
                "description":"Shooters let players use weapons to engage in the action, with the goal usually being to take out enemies or opposing players.",
                "id":3,
                "name":"shooter"
            },
            {
                "description":"Puzzle or logic games usually take place on a single screen or playfield and require the player to solve a problem to advance the action.",
                "id":4,
                "name":"puzzle"
            }
        ],
        "success":true,
        "total_categories":2
        }
    ```

### Get `/api/categories/<category_id>`

* General

  * Returns the details of a category, and a success value.

* Sample

  * Request: `curl -H "Authorization: ${TOKEN}" https://fsnd-gamify.herokuapp.com/api/categories/3`

  * Response:

    ```JSON
    {
        "category":{
            "description":"Shooters let players use weapons to engage in the action, with the goal usually being to take out enemies or opposing players.",
            "id":3,
            "name":"shooter"
        },
        "games":[
            {
                "age_rating":"+16",
                "category_id":3,
                "developer_id":2,
                "id":4,
                "image_link":"https://images-na.ssl-images-amazon.com/images/I/812HBc8O%2BUL._SY445_.jpg",
                "name":"overwatch"
            },
            {
                "age_rating":"+18",
                "category_id":3,
                "developer_id":4,
                "id":3,
                "image_link":"https://images.goodgam.es/8RomeOKHaf8/enlarge:1/plain/covers/682-valorant-cover.jpg",
                "name":"valorant"
            }
        ],
        "success":true,
        "total_games":2
    }
    ```

### DELETE `/api/categories/{category_id}`

* General

  * Deletes the category of the given ID if it exists along with associated games. Returns the ID of the deleted category, success value, and categories list.

* Sample

  * Request: `curl -H "Authorization: ${TOKEN}" -X DELETE https://fsnd-gamify.herokuapp.com/api/categories/4`

  * Response:

    ```JSON
    {
        "categories":[
            {
                "description":"Shooters let players use weapons to engage in the action, with the goal usually being to take out enemies or opposing players.",
                "id":3,
                "name":"shooter"
            }
        ],
        "deleted":4,
        "success":true
    }
    ```

### POST `/api/categories`

* General

  * Creates a new category using the submitted name, and description. Returns the newly created category and a success value.

* Sample

  * Request: `curl -H "Content-Type: application/json" -H "Authorization: ${TOKEN}" -d '{"name": "sports", "description": "Sports games simulate sports like golf, football, basketball, baseball, and soccer. They can also include Olympic sports like skiing, and even pub sports like darts and pool."}' -X POST https://fsnd-gamify.herokuapp.com/api/categories`

  * Response:

    ```JSON
    {
        "category":{
            "description":"Sports games simulate sports like golf, football, basketball, baseball, and soccer. They can also include Olympic sports like skiing, and even pub sports like darts and pool.",
            "id":5,
            "name":"sports"
        },
        "success":true
    }
    ```

### PATCH `/api/categories/<category_id>`

* General

  * Edits the category of the given ID if it exists using the submitted name, and description. Returns the ID of the updated category, success value, and categories list.

* Sample

  * Request: `curl -H "Content-Type: application/json" -H "Authorization: ${TOKEN}" -d '{"name": "strategy", "description": "With gameplay is based on traditional strategy board games, strategy games give players a godlike access to the world and its resources. These games require players to use carefully developed strategy and tactics to overcome challenges."}' -X PATCH https://fsnd-gamify.herokuapp.com/api/categories/5`

  * Response:

    ```JSON
    {
        "categories":[
            {
                "description":"Shooters let players use weapons to engage in the action, with the goal usually being to take out enemies or opposing players.",
                "id":3,
                "name":"shooter"
            },
            {
                "description":"With gameplay is based on traditional strategy board games, strategy games give players a godlike access to the world and its resources. These games require players to use carefully developed strategy and tactics to overcome challenges.",
                "id":5,
                "name":"strategy"
            }
        ],
        "success":true,
        "updated":"5"
    }
    ```

### Get `/api/developers`

* General

  * Returns a list of developer objects.

* Sample

  * Request: `curl https://fsnd-gamify.herokuapp.com/api/developers`

  * Response:

    ```JSON
    {
        "developers":[
            {
                "id":2,
                "name":"blizzard",
                "website":"www.blizzard.com"
            },
            {
                "id":3,
                "name":"activision",
                "website":"www.activision.com"
            },
            {
                "id":4,
                "name":"riot",
                "website":"https://www.riotgames.com"
            }
        ],
        "success":true,
        "total_developers":3
    }
    ```

### Get `/api/developers/<developer_id>`

* General

  * Returns the details of a developer, and a success value.

* Sample

  * Request: `curl -H "Authorization: ${TOKEN}" https://fsnd-gamify.herokuapp.com/api/developers/2`

  * Response:

    ```JSON
    {
        "developer":{
            "id":2,
            "name":"blizzard",
            "website":"www.blizzard.com"
        },
        "games":[
            {
                "age_rating":"+16",
                "category_id":3,
                "developer_id":2,
                "id":4,
                "image_link":"https://images-na.ssl-images-amazon.com/images/I/812HBc8O%2BUL._SY445_.jpg",
                "name":"overwatch"
            }
        ],
        "success":true,
        "total_games":1
    }
    ```

### DELETE `/api/developers/{developer_id}`

* General

  * Deletes the developer of the given ID if it exists along with associated games. Returns the ID of the deleted developer, success value, and developers list.

* Sample

  * Request: `curl -H "Authorization: ${TOKEN}" -X DELETE https://fsnd-gamify.herokuapp.com/api/developers/3`

  * Response:

    ```JSON
    {
        "deleted":"3",
        "developers":[
            {
                "id":2,
                "name":"blizzard",
                "website":"www.blizzard.com"
            },
            {
                "id":4,
                "name":"riot",
                "website":"https://www.riotgames.com"
            }
        ],
        "success":true
    }
    ```

### POST `/api/developers`

* General

  * Creates a new developer using the submitted name, and website. Returns the newly created developer and a success value.

* Sample

  * Request: `curl -H "Content-Type: application/json" -H "Authorization: ${TOKEN}" -d '{"name": "bungie", "website": "www.bungie.net"}' -X POST https://fsnd-gamify.herokuapp.com/api/developers`

  * Response:

    ```JSON
    {
        "developer":{
            "id":5,
            "name":"bungie",
            "website":"www.bungie.net"
        },
        "success":true}
    ```

### PATCH `/api/developers/<developer_id>`

* General

  * Edits the developer of the given ID if it exists using the submitted name, and website. Returns the ID of the updated developer, success value, and developers list.

* Sample

  * Request: `curl -H "Content-Type: application/json" -H "Authorization: ${TOKEN}" -d '{"name": "ea", "website": "www.ea.com"}' -X PATCH https://fsnd-gamify.herokuapp.com/api/developers/5`

  * Response:

    ```JSON
    {
        "developers":[
            {
                "id":2,
                "name":"blizzard",
                "website":"www.blizzard.com"
            },
            {
                "id":4,
                "name":"riot",
                "website":"https://www.riotgames.com"
            },
            {
                "id":5,
                "name":"ea",
                "website":"www.ea.com"
            }
        ],
        "success":true,
        "updated":"5"
    }

    ```