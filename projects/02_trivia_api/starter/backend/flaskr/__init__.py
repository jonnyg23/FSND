import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#----------------------------------------------------------------------------#
    # Custom Methods
#----------------------------------------------------------------------------#

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

#----------------------------------------------------------------------------#
    # Setup Application & Create API Endpoints
#----------------------------------------------------------------------------#

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    #'''
    #Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    #'''
    CORS(app)
  
    #'''
    #CORS header
    #Use the after_request decorator to set Access-Control-Allow
    #'''
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
    
        response.headers.add('Access-Control-Allow-Headers','Content-Type.Authorization,true')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        return response
  
    #''' 
    #Create an endpoint to handle GET requests 
    #for all available categories.
    #'''
  
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
            'categories': {category.id: category.type for category in categories}
        })
  
  
  
    #'''
    #Create an endpoint to handle GET requests for questions, 
    #including pagination (every 10 questions). 
    #This endpoint should return a list of questions, 
    #number of total questions, current category, categories. 
  
    #TEST: At this point, when you start the application
    #you should see questions and categories generated,
    #ten questions per page and pagination at the bottom of the screen for three pages.
    #Clicking on the page numbers should update the questions. 
    #'''
    
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        """
        Retrieves paginated questions from database.
    
        Tested with:
          Success:
              - test_get_paginated_questions
          Error:
              - test_404_delete_question
        """
        selection = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        current_questions = paginate_questions(request, selection)
    
        if len(current_questions) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in categories},
            'current_category': None
        })
  
    #''' 
    #Create an endpoint to DELETE question using a question ID. 
  
    #TEST: When you click the trash icon next to a question, the question will be removed.
    #This removal will persist in the database and when you refresh the page. 
    #'''
  
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Deletes a question from database.
    
        Tested with:
            Success:
                - test_delete_question
            Error:
                - test_422_sent_deleting_non_existing_question
        """
        # Query the question id from database
        question = Question.query.filter(Question.id == question_id).one_or_none()
    
        if not question:
            # If no question found with id, raise 404
            abort(400)
        
        try:
            # Delete the question by referencing question id
            question.delete()
    
            return jsonify({
                'success': True,
                'deleted': question_id
            })
    
        except:
            abort(422)
    
  
  
    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
  
    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
  
    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
  
  
    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
  
    '''
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400
  
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404
  
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405
  
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422
  
    
    return app
  
      