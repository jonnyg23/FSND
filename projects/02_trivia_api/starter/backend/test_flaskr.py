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
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_non_existing_category(self):
        res = self.client().get('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

#----------------------------------------------------------------------------#
# Test if questions and categories are generated 10 questions per page and pagination at bottom of screen for 3 pages on starting application
#----------------------------------------------------------------------------#
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
#----------------------------------------------------------------------------#
    # Test if clicking trash icon next to question removes question from database and on page refresh
#----------------------------------------------------------------------------#
    def test_delete_question(self):
        # Found Question objects' input datatypes from psql trivia_test database tables
        question = Question(question='test question', answer='test answer', category=1, difficulty=1)
        question_id = question.id
        question.insert() # Add and commit to database session

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question_query = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], str(question_id))
        self.assertEqual(question_query, None)  

    def test_422_sent_deleting_non_existing_question(self):
        res = self.client().delete('/questions/non_existing_question')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

#----------------------------------------------------------------------------#
    # Test adding a question
#----------------------------------------------------------------------------#



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()