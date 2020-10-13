import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# ----------------------------------------------------------------------------#
# Custom Methods
# ----------------------------------------------------------------------------#


def error_message(error, text):
    """
    Gives default or custom text for the error.
    --------------------
    Inputs <datatype>:
        - error <Error Object>: The error code
        - text <string>: Custom error text if error has no message
    Returns <datatype>:
        - error description <string>: The custom error description or default
    """
    try:
        return error.description['message']
    except TypeError:
        return text


def paginate_questions(request, selection):
    """
    Paginates Questions
    --------------------
    Inputs <datatype>:
        - request <HTTP Object>: This is the request for getting page number
        - selection <list>: Question selection from database

    Returns <datatype>:
        - current_questions <list>: 10 questions at a time from database
    """
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

# ----------------------------------------------------------------------------#
    # Setup Application & Create API Endpoints
# ----------------------------------------------------------------------------#


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # '''
    # Set up CORS. Allow '*' for origins.
    # Delete the sample route after completing the TODOs
    # '''
    CORS(app)

    # '''
    # CORS header
    # Use the after_request decorator to set Access-Control-Allow
    # '''
    @app.after_request
    def after_request(response):
        """
        Used to set Access-Control-Allow.
        --------------------
        Inputs <datatype>:
          - None

        Returns <datatype>:
          - response <Response Object>
        """

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type.Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # '''
    # Create an endpoint to handle GET requests
    # for all available categories.
    # '''

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        """
        Retrieves categories from database.

        Tested with:
          Success:
              - test_get_categories
          Error:
              - test_404_sent_requesting_non_existing_category
        """

        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type
                           for category in categories}
        })

    # '''
    # Create an endpoint to handle GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.

    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination at the bottom of
    # the screen for three pages.
    # Clicking on the page numbers should update the questions.
    # '''

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        """
        Retrieves paginated questions from database.

        Tested with:
          Success:
              - test_get_paginated_questions
          Error:
              - test_404_sent_requesting_beyond_valid_pag
        """
        selection = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        categories_return = {
            cat.id: cat.type for cat in categories
            }

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories_return,
            'current_category': None
        })

    # '''
    # Create an endpoint to DELETE question using a question ID.

    # TEST: When you click the trash icon next to a question,
    # the question will be removed.
    # This removal will persist in the database and when you refresh the page.
    # '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Deletes a question from database.

        Tested with:
            Success:
                - test_delete_question
            Error:
                - test_404_delete_question
        """
        # Query the question id from database
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if not question:
            # If no question found with id, raise 404
            abort(404, {'message':
                        f'Question ID: {question_id} does not exist.'})

        try:
            # Delete the question by referencing question id
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except:
            abort(422)

    # '''
    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.

    # TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question
    # will appear at the end of the last page
    # of the questions list in the "List" tab.
    # '''
    # And.....
    # '''
    # Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    # '''

    @app.route('/questions', methods=['POST'])
    def add_or_search_question():
        """
        Adds question to database or searches for a question.

        Tested with:
            Success:
                - test_add_question
                - test_search_question
            Error:
                - test_400_add_question
                - test_404_search_question
        """
        body = request.get_json()

        if not body:
            abort(400, {'message': 'Invalid JSON body'})

        search_term = body.get('search_term', None)

        # Query search_term if JSON body contains search term
        if search_term:
            search_results = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            # Return 404 if search_term not found in questions
            if not search_results:
                abort(
                    404,
                    {
                        'message':
                        f'No questions with the search term: {search_term}'
                    }
                )

            questions = [question.format() for question in search_results]
            selection = Question.query.order_by(Question.id).all()

            category_query = Category.query.all()
            categories = [category.format() for category in category_query]

            # If search_term successfully found questions, return JSON
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(selection),
                'current_category': categories
            })

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        # Return 400 error if any parameters are missing
        if not new_question:
            abort(400, {'message': 'Question parameter is missing.'})

        if not new_answer:
            abort(400, {'message': 'Answer parameter is missing.'})

        if not new_category:
            abort(400, {'message': 'Category parameter is missing.'})

        if not new_difficulty:
            abort(400, {'message': 'Difficulty parameter is missing.'})

        # Attempt adding new question to database
        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(selection)
            })

        except:
            abort(422)

    # '''
    # Create a GET endpoint to get questions based on category.

    # TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    # '''

    @app.route('/categories/<string:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        """
        Retrieves questions from database based on desired category.

        Tested with:
            Success:
                - test_get_questions_by_category

            Error:
                - test_400_get_questions_by_category
        """
        questions = Question.query.filter(Question.category == str(
            category_id)).order_by(Question.id).all()

        # Check if there are questions with the category_id, if not abort 400
        if not questions:
            abort(
                400,
                {
                    'message':
                    f'Questions with the {category_id} category do not exist.'
                }
            )

        # Check if selected page contains questions, if not abort 404
        current_questions = paginate_questions(request, questions)
        if not current_questions:
            abort(
                404, {'message':
                      'Selected page does not contain any questions.'})

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': category_id
        })

    # '''
    # Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.

    # TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    # '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """
        Endpoint used to get questions in order to play the quiz.

        Tested with:
            Success:
                - test_play_quiz

            Error:
                - test_422_play_quiz
                - test_405_play_quiz
        """
        try:
            body = request.get_json()
            # print(f'THIS IS THE BODY: {body}')

            # If JSON body not given or there are empty parameters -
            # raise 422 error
            if not body:
                abort(422, {'message': 'unprocessable'})

            # Pre-allocate variables from JSON body
            previous_questions = body.get('previous_questions', None)
            current_category = body.get('quiz_category', None)

            # If the "ALL" variable is selected, the 'id' retrieved from the
            # 'quiz_category' frontend attribute should be equal to 0. This is
            # basically another way of saying 'type'== 'click'.
            if current_category['id'] == 0:
                # Query database for all questions that do not exist in the
                # previous_questions list, hence the .notin_
                questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()

            # If an actual category is selected and not "ALL", then query the
            # database for questions with the matching category id.
            else:
                questions = Question.query\
                    .filter_by(category=current_category['id'])\
                    .filter(Question.id.notin_((previous_questions)))\
                    .all()

            # Choose a random question from list of questions if list is not
            # empty.
            if questions:
                # Out of the list of questions,
                # pick a random question using the
                # random library choice method and then format it.
                randomized_question = random.choice(questions).format()

            else:
                randomized_question = None

            # print(f'randomized_question: {randomized_question}')

            return jsonify({
                'success': True,
                'question': randomized_question
            })

        except:
            abort(422, {'message': 'unprocessable'})

    # '''
    # Create error handlers for all expected errors
    # including 404 and 422.
    # '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': error_message(error, 'bad request')
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': error_message(error, 'resource not found')
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': error_message(error, 'method not allowed')
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': error_message(error, 'unprocessable')
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
