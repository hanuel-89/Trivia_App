from crypt import methods
import json
from nis import cat
import os
from tokenize import Floatnumber
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    stop = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    return questions[start:stop]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()

            if len(categories) == 0:
                abort(404)

            # print(categories.formate())

            tmp_category_format = [category.format_id_type()
                                   for category in categories]

            formatted_category = {}
            for key_pair in tmp_category_format:
                for key, value in key_pair.items():
                    formatted_category[key] = value

            return jsonify(
                {
                    "success": True,
                    "categories": formatted_category,
                    "total_categories": len(categories)
                }
            ), formatted_category
        except Exception:
            abort(422)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.


    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)
        _, formatted_category = get_categories()

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": formatted_category,
                "current_category": "History"
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            #selection = Question.query.order_by(Question.id).all()
            #current_questionss = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question.id,
                    "total_questions": len(Question.query.all()),
                }
            )
        except Exception:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        search = body.get('searchTerm', None)
        categories = Category.query.all()

        try:
            if search:
                selection = Question.query.filter(
                    Question.question.ilike(f"%{search}%")).all()
                if len(selection) == 0:
                    abort(404)
                questions_found = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "questions": questions_found,
                        "total_questions": len(selection),
                        # "current_category": {category.id: category.type for category in categories}

                    }
                )

            else:
                question = Question(question=new_question, answer=new_answer,
                                    category=new_category, difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                _, formatted_category = get_categories()

                return jsonify(
                    {
                        "success": True,
                        #"questions": current_questions,
                        "total_questions": len(selection),
                        "posted_question_Id": question.id,
                        "posted": Question.query.filter(Question.id==question.id).one().format()

                    }
                )
        except Exception:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        try:
            selection = Question.query.filter(Question.category == id).all()
            if len(selection) == 0:
                abort(404)
            current_questions = paginate_questions(request, selection)

            _, formatted_category = get_categories()
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection),
                    "current_category": id
                }
            )
        except Exception:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['GET', 'POST'])
    def next_question():
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        print(previous_questions)
        print(quiz_category)
        quiz_category_id = quiz_category['id']
        try:
            if quiz_category_id == 0:
                selection = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                category = Category.query.get(quiz_category_id)
                if category is not None:
                    selection = Question.query.filter(Question.id.notin_(previous_questions)).filter(
                        Question.category == quiz_category_id).all()
            current_question = None
            if len(selection) > 0:
                current_question = random.choice(selection).format()
            return jsonify(
                {
                    "success": True,
                    "question": current_question,
                    "totalQuesitons": len(Question.query.all())
                }
            )

        except Exception:
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "method not allowed"}),
            405,
        )

    return app
