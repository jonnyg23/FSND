# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Documentation

This RESTful API documentation will reveal not only what endpoints there are, but also give an example of responses to each method request.

### Getting Started

* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, **http://127.0.0.1:5000/**, which is set as a proxy in the frontend configuration. This is the domain which must be used when making API requests via `postman` or `curl`.
* Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```js
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return the five error type default responses when requests fail (unless custom response is assigned):

* 400: Bad Request
* 404: Resource Not Found
* 405: Method Not Allowed
* 422: Not Processable
* 500: Internal Server Error

### Table of Endpoints

Below is a table of the methods allowed for each of the 3 endpoints.

| Endpoints   |     | Methods |        |
|-------------|-----|---------|--------|
|             | GET | POST    | DELETE |
| /questions  | X   | X       | X      |
| /categories | X   |         |        |
| /quizzes    |     | X       |        |

### Endpoint Table of Contents

1. Questions:
    * [GET /questions](#get_questions)
    * [POST /questions](#post_questions)
    * [DELETE /questions/<question_id>](#delete_questions)
2. Categories:
    * [GET /categories](#get_categories)
    * [GET /categories/<category_id>/questions](#get_categories_questions)
3. Quizzes:
    * [POST /quizzes](#post_quizzes)

# <a name="get_questions"></a>
### GET /questions

Retrieves paginated questions from database:
```bash
$ curl -X GET http://127.0.0.1:5000/questions?page=2
```

**Request Parameters**: `None`  

**Returns**:  
1. List of dictionary of questions with:  
    * **integer** `id`
    * **string** `question`
    * **string** `answer`
    * **string** `category`
    * **integer** `difficulty`
2. **boolean** `success`
3. **integer** `total_questions`
4. **list** `categories`
5. **list** `current_category`

#### Example Response

```js
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 

    [...]

  ], 
  "success": true, 
  "total_questions": 16
}
```

#### Errors

When attempting to get a page that has no questions, the request and response may appear as such:

Request
```bash
$ curl -X GET http://127.0.0.1:5000/questions?page=1000
```
Response
```js
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```

# <a name="post_questions"></a>
### POST /questions
This endpoint allows searching, as well as creating new questions. These requests using `curl` make look as such:  

Adding a New Question
```bash
$ curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "New Question", "category" : "2" , "answer" : "New Answer", "difficulty" : 3 }' -H 'Content-Type: application/json'
```

Searching for Questions
```bash
$ curl -X POST http://127.0.0.1:5000/questions -d '{"search_term" : "title"}' -H 'Content-Type: application/json'
```

Attempts to search for questions using the search term, however, if no search term is given, then it will attempt to add a question to the database.


**Request Parameters**:  
1. If searching for questions:  
    * **string** `search_term`  
2. If adding new question:  
    * **string** `question`
    * **string** `answer`
    * **string** `category`
    * **integer** `difficulty`
  
**Returns**:  
1. If searching for questions:
    * **boolean** `success`
    * List of dictionary of questions with:  
      * **integer** `id`
      * **string** `question`
      * **string** `answer`
      * **string** `category`
      * **integer** `difficulty`
    * **integer** `total_questions`
    * List of dictionary of current_category which contains:
      * **integer** `id`
      * **string** `type`
2. If adding new question:
    * **boolean** `success`
    * **integer** `created` inserted question id
    * List of dictionary of questions with:  
      * **integer** `id`
      * **string** `question`
      * **string** `answer`
      * **string** `category`
      * **integer** `difficulty`
    * **integer** `total_questions`

#### Example Response

Adding a New Question
```js
{
  "created": 25, 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    
    [...]

  ], 
  "success": true, 
  "total_questions": 18
}

```

Searching for Questions
```js
{
  "current_category": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 17
}
```

#### Errors

Error adding Questions:  
* When adding a question, if not all parameters are included such as 'difficulty', then a `400 error` will be raised. This is viewed below with the following request and response.

Request
```bash
$ curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "New Question", "answer" : "New Answer" , "category" : 2 }' -H 'Content-Type: application/json'
```

Response
```js
{
  "error": 400, 
  "message": "Difficulty parameter is missing.", 
  "success": false
}
```

Error Searching for Questions:
* If a question does not exist with the given search term, then a 404 error will be raised.

Request
```bash
$ curl -X POST http://127.0.0.1:5000/questions -d '{"search_term" : "this question does not exist"}' -H'Content-Type: application/json' 
```

Response
```js
{
  "error": 404, 
  "message": "There are no questions with the search term: this question does not exist", 
  "success": false
}
```

# <a name="delete_questions"></a>
### DELETE /questions/<question_id>

This allows for deleting a question from the database. A `curl` request would look as such:  

```bash
$ curl -X DELETE http://127.0.0.1:5000/questions/10
```

**Request Parameters**: `None`  

**Returns**:  
1. **boolean** `success`
2. **integer** `deleted`

#### Example Response

Response
```js
{
  "deleted": 10, 
  "success": true
}
```

#### Errors

The response will be a `400 error` if the question id does not exist. Below is the request and response for deleting a question with an id of 2. This id does not exist.

Request
```bash
$ curl -X DELETE http://127.0.0.1:5000/questions/2
```

Response
```js
{
  "error": 404, 
  "message": "Question ID: 2 does not exist.", 
  "success": false
}
```

# <a name="get_categories"></a>
### GET /categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category. A `curl` request example is seen below.
```bash
$ curl -X GET http://127.0.0.1:5000/categories
```

Request Parameters: None  

Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.  

#### Example Response

```js
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### Errors

This endpoint does not raise an error.

# <a name="get_categories_questions"></a>
### GET /categories/<category_id>/questions

This gets all questions found in the desired category.

```bash
$ curl -X GET http://127.0.0.1:5000/categories/1/questions?page=1
```

**Request Parameters**: `None`  

**Returns**:  
1. **boolean** `success`
2. List of dictionary of questions with:  
    * **integer** `id`
    * **string** `question`
    * **string** `answer`
    * **string** `category`
    * **integer** `difficulty`
3. **integer** `total_questions`
4. **list** `current_category`

#### Example Response

```js
{
  "current_category": "1", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Yes it is!", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "Is this a test question?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}

```

#### Errors

Two errors are possible for requesting questions in a desired category.

1. `404 Error` occurs if category is correct, but page number does not exist. Request and response are as follows:

Request
```bash
$ curl -X GET http://127.0.0.1:5000/categories/1/questions?page=10
```

Response
```js
{
  "error": 404, 
  "message": "Selected page does not contain any questions.", 
  "success": false
}
```

2. `400 Error` occurs if page number exists, but category does not. Request and response are as follows:

Request
```bash
$ curl -X GET http://127.0.0.1:5000/categories/999999999/questions?page=1
```

Response
```js
{
  "error": 400, 
  "message": "Questions with the 999999999 category do not exist.", 
  "success": false
}
```

# <a name="post_quizzes"></a>
### POST /quizzes

Play the Trivia Game!
```bash
$ curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [1,2,3], "quiz_category" : {"type" : "Art", "id" : "2"}} ' -H 'Content-Type: application/json'
```

**Request Parameters**:  
1. **list** `previous_questions`
2. **integer** `quiz_category` 

**Returns**:  
1. **boolean** `success`
2. One question as dictionary:  
    * **integer** `id`
    * **string** `question`
    * **string** `answer`
    * **string** `category`
    * **integer** `difficulty`

#### Example Response

```js
{
  "question": {
    "answer": "One", 
    "category": 2, 
    "difficulty": 4, 
    "id": 18, 
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }, 
  "success": true
}
```

#### Errors

`400 error` raised if JSON body is invalid. This request and response are shown below:  

Request
```bash
$ curl -X POST http://127.0.0.1:5000/quizzes
```

Response
```js
{
  "error": 400, 
  "message": "Use JSON body with previous question.", 
  "success": false
}
```


