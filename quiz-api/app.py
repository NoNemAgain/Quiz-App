from distutils.log import error
from flask import Flask, jsonify, request
from Utils import Config ,jwt_utils
import sqlite3
from Model import questionModel
from flask_cors import CORS
from Service import QuestionService , QuizService,ParticipationService
app = Flask(__name__)
CORS(app)

# -*- coding: utf-8 -*-
         


@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"


@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    
    if payload['password'] == "Vive l'ESIEE !" :
        return jsonify({'token':jwt_utils.build_token()})
    else :
        return '', 401

# Question
@app.route('/questions/<position>', methods=['GET'])
def GetQuestion(position):
        try:
                question =QuestionService.getQuestionByPosition(position).toJSON()
                return question.encode('utf8') ,200
        except Exception:
                return '',404
                

@app.route('/questions/<position>', methods=['PUT'])
def UpdateQuestion(position):
        try:
                if request.headers.get('Authorization') is None :
                        return '',401
                updatedQuestion =QuestionService.convertJsonToQuestion(request.get_json())
                return QuestionService.updateQuestion(position,updatedQuestion)
        except Exception:
                return '',404

@app.route('/questions/<position>', methods=['DELETE'])
def DeleteQuestion(position):
        try:
                if request.headers.get('Authorization') is None :
                        return '',401
                return QuestionService.deleteQuestion(position)
        except Exception:
                return '',404
        
@app.route('/questions', methods=['POST'])
def addQuestion():
        try:
                if request.headers.get('Authorization') is None :
                        return '',401
                question =QuestionService.convertJsonToQuestion(request.get_json())
                return QuestionService.createQuestion(question)
        except Exception:
                return '',400
# Participation

@app.route('/participations', methods=['POST'])
def addParticipation():
        try:    
                # if request.headers.get('Authorization') is None :
                #         return '',401
                participation =ParticipationService.convertJsonToParticipation(request.get_json())
                return ParticipationService.createParticipation(participation)
        except Exception:
                return '',400

@app.route('/participations', methods=['DELETE'])
def DeleteAllParticipiation():
        try:
                # if request.headers.get('Authorization') is None :
                #         return '',401
                return ParticipationService.deleteAllParticipiation()
        except Exception:
                return '',404
@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
        try:
                quiz =QuizService.getQuiz().toJSON()
                return quiz.encode('utf8') ,200
        except Exception:
                return '',404
if __name__ == "__main__":
    app.run()
        # app.run(host='0.0.0.0', port=5000)