import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    # Set up the test
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f"postgres://localhost:5432/{self.database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "Who is the president of Nigeria?", "answer": "Buhari", "difficulty": 1, "category": 4}
        self.new_search = {"searchTerm": "What"}
        self.no_search = {"searchTerm": "XXX"}
        self.quizzes = {'previous_questions': [1, 4, 20, 15], 'quiz_category': {"id": 3, "type": "Geography"}}

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Test the get_categories endpoint
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertTrue(len(data["categories"]))

    # Test the get_questions endpoint
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    # Test 404 error when the page requested is not available
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # Test post_question endpoint
    def test_post_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["posted"])

    # test posting questions to the wrong endpoint
    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/questions/45", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    # Test the delete endpoint
    def test_delete_question(self):
        res = self.client().delete("/questions/10")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 10)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(question, None)

    # Test 422 for question ids that don't exist
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # Test getting questions based on category
    def test_get_question_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        questions = Question.query.filter(Question.category == 1).all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), len(questions))
        self.assertEqual(data["current_category"], 1)

    # Test 422 error for categories that don't exist
    def test_422_if_category_does_not_exist(self):
        res = self.client().get("/categories/100/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # Test the search function of the '/questions' endpoint
    def test_search_questions(self):
        res = self.client().post('/questions', json=self.new_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertNotEqual(len(data['questions']), 1)
        self.assertTrue(data["questions"])

    # Test fetching the next questions based on present category
    def test_next_question(self):
        res = self.client().post('/quizzes', json=self.quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])
        self.assertNotIn(data["question"]["id"], self.quizzes['previous_questions'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()