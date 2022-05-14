from distutils.log import error
from flask import Flask, jsonify, request
from Utils import Config ,jwt_utils
import sqlite3
from Model import questionModel
from Service import QuestionService
app = Flask(__name__)


         


@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/questions/<position>', methods=['GET'])
def GetQuestion(position):
        try:
                Result =QuestionService.getQuestionByPosition(position)
                jsonResult = QuestionService.convertQuestionToJson(Result)
                return jsonResult.encode('utf8').decode("utf_8") ,200
        except Exception:
                return '',404
                
     


@app.route('/questions/<oldPositionQuestion>', methods=['PUT'])
def UpdateQuestion(oldPositionQuestion):
        try:
                if request.headers.get('Authorization') is None :
                        return '',401
                updatedQuestion =QuestionService.convertJsonToQuestion(request.get_json())
                return QuestionService.updateQuestion(oldPositionQuestion,updatedQuestion)
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
        
        

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    
    if payload['password'] == "Vive l'ESIEE !" :
        return jsonify({'token':jwt_utils.build_token()})
    else :
        return '', 401
@app.route('/questions', methods=['POST'])
def addQuestion():
        try:
                if request.headers.get('Authorization') is None :
                        return '',401
                question =QuestionService.convertJsonToQuestion(request.get_json())
                return QuestionService.createQuestion(question)
        except Exception:
                return '',400
    

if __name__ == "__main__":
    app.run(ssl_context='adhoc')