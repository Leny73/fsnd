import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in questions]
    current_questions = formatted_questions[start:end]
    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = {category.id: category.type for category in categories}
    if len(categories) == 0:
        abort(404)  
    else:
        return jsonify({
            'success': True,
            'categories': formatted_categories,    
            'total': len(Category.query.all())
        })

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    questions = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
    current_questions = paginate_questions(request, questions)
    print(current_questions)
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = {category.id: category.type for category in categories}
    print(formatted_categories)
    try:
        category = Category.query.filter(Category.id == category_id).one_or_none()
        print(category)
        formatted_category = {category.id: category.type }
        if formatted_category is None:
            abort(404)

        if len(current_questions) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'questions': current_questions,    
                'total_questions': len(Question.query.all()),
                'categories': formatted_categories,
                'current_category': formatted_category,
            })
    except:
        abort(400)
  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = {category.id: category.type for category in categories}

    if len(current_questions) == 0:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'questions': current_questions,    
            'total_questions': len(Question.query.all()),
            'categories': formatted_categories,
            'current_category': None

        })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      try:
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'success': True,
            'deleted': question_id
        })
      except:
        abort(422)


  @app.route('/questions', methods=['POST'])
  def add_question():
      body = request.get_json()
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_difficulty = body.get('difficulty', None)
      new_category = body.get('category', None)
      search = body.get('searchTerm', None)

      try:
          if search:
            selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection.all())
            })
          else:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()

            return jsonify({
                'success': True,
            })
      except:
          abort(422)

  @app.route("/quizzes", methods=["POST"])
  def start_quiz():
    body = request.get_json()
    previous_questions = body.get("previous_questions", [])
    quiz_category = body.get("quiz_category", None)

    try:
        category_id = int(quiz_category['id'])
        if category_id == 0:
            quiz = Question.query.all()
        else:
            quiz = Question.query.filter_by(category=category_id).all()
        selected = []
        for question in quiz:
            if question.id not in previous_questions:
                selected.append(question.format())
        if len(selected) != 0:
            result = random.choice(selected)
            return jsonify({
                'question': result,
                'success': True,
                })
        else:
            return jsonify({
                'question': None,
                'success': False
                })
    except:
        abort(422)

  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Resource not found!"
            }), 404

  @app.errorhandler(422)
  def not_found(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable!"
            }), 422

  @app.errorhandler(400)
  def not_found(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad request!"
            }), 400

  @app.errorhandler(405)
  def not_found(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "Method not allowed!"
            }), 405
  
  return app

    
