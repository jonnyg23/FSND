import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('THEJAGSTER','','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
#----------------------------------------------------------------------------#
    # Used Test-Driven-Development in the making of this API
    
    # Test if '/categories' endpoint can handle GET requests & sends 404 error for a non existing category
#----------------------------------------------------------------------------#
    def test_get_categories(self):
        """Test for retrieve_categories() GET /categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_non_existing_category(self):
        """Test retrieve_categories() for non-existing category - prompt error 404"""
        res = self.client().get('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

#----------------------------------------------------------------------------#
# Test if questions and categories are generated 10 questions per page and pagination at bottom of screen for 3 pages on starting application
#----------------------------------------------------------------------------#
    def test_get_paginated_questions(self):
        """Test retrieve_questions() GET /questions"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_beyond_valid_page(self):
        """Test retrieve_questions() for invalid page request - prompt error 404"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
#----------------------------------------------------------------------------#
    # Test if clicking trash icon next to question removes question from database and on page refresh
#----------------------------------------------------------------------------#
    def test_delete_question(self):
        """Test delete_question() DELETE /questions/<int:question_id>"""
        # Found Question objects' input datatypes from psql trivia_test database tables
        question = Question(question='test question', answer='test answer', category=1, difficulty=1)
        question.insert() # Add and commit to database session
        question_id = question.id

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question_query = Question.query.filter(Question.id == question_id).one_or_none()
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question_query, None)  

    def test_404_delete_question(self):
        """Test delete_question() for non-existing ID - prompt error 404"""
        res = self.client().delete(f'/questions/{123456789}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'Question ID: {123456789} does not exist.')

#----------------------------------------------------------------------------#
    # Test creating an endpoint to POST a new question. WHen submitting a question on "Add" tab, form will clear and question will appear at end of last page of questions list in the "List" tab. Tests POST /questions
#----------------------------------------------------------------------------#
    def test_add_question(self):
        """Test add_or_search_question() POST /questions"""
        # Create new question json
        new_question = {
            'question': 'New Question',
            'answer': 'New Answer',
            'category': 2,
            'difficulty': 3
        }
        # Count total questions to compare after POST
        question_count_initial = len(Question.query.all())
        
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        question_count_final = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question_count_final, question_count_initial + 1)


    def test_400_add_question(self):
        """Test add_or_search_question() for missing parameter - prompt error 400"""
        # Create new question with missing parameter -> difficulty
        new_question = {
            'question': 'New Question',
            'answer': 'New Answer',
            'category': 2,
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Difficulty parameter is missing.')

#----------------------------------------------------------------------------#
    # Test searching by any phrase. The question list will update to include only questions that include that string within question. Tests POST /questions for search term
#----------------------------------------------------------------------------#
    def test_search_question(self):
        """Test add_or_search_question() POST /questions search term"""
        search_term = {
            'search_term': 'title'
        }

        res = self.client().post('/questions', json=search_term)
        data = json.loads(res.data)
        data_length = len(data['questions'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data_length > 0)
        self.assertTrue(data['total_questions'] > 0)

    def test_404_search_question(self):
        """Test add_or_search_question() for non-existing search term - prompt error 404"""
        search_term = {
            'search_term': 'this question does not exist'
        }
        
        res = self.client().post('/questions', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'There are no questions with the search term: this question does not exist')

#----------------------------------------------------------------------------#
    # Test GET endpoint to get questions based on category. Clicking on one of the categories in the left column in the "List" tab will cause only questions of that category to be shown. Tests GET /categories/category_id/questions
#----------------------------------------------------------------------------#
    def test_get_questions_by_category(self):
        """Test retrieve_questions_by_category() GET /category/category_id/questions"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['questions'] > 0))
        self.assertTrue(data['total_questions'] > 0)

    def test_400_get_questions_by_category(self):
        """Test retrieve_questions_by_category() for questions with found category - prompt error 400"""
        res = self.client().get('/categories/invalid_category/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Questions with the invalid_category category do not exist.')

#----------------------------------------------------------------------------#
    # Test POST endpoint to get questions to play the quiz. Takes category and previous question paramters and returns a random question within the given category if provided, and that is not one of the previous questions. Tests POST /quizzes
#----------------------------------------------------------------------------#
    def test_play_quiz_with_category(self):
        """Test play_quiz() POST /quizzes with a category"""
        pass

    def test_play_quiz_without_category(self):
        """Test play_quiz() POST /quizzes with no category"""
        pass
    
    def test_400_play_quiz(self):
        """Test play_quiz() if JSON body exists - prompt error 400"""
        pass

    def test_405_play_quiz(self):
        """Test play_quiz() if invalid method is allowed - prompt error 405"""
        pass

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()