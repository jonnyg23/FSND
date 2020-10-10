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
        """Test retrieve_categories() for non-existing category"""
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
        """Test retrieve_questions() for invalid page request"""
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
        """Test delete_question() for non-existing ID"""
        res = self.client().delete(f'/questions/{123456789}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], f'Question ID: {123456789} does not exist.')

#----------------------------------------------------------------------------#
    # Test adding a question
#----------------------------------------------------------------------------#



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()