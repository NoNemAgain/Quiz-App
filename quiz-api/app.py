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
        pos =position
        result =QuestionService.getQuestionByPosition(pos)  
        jsonResult = QuestionService.convertQuestionToJson(result)
        return jsonResult.encode('utf8').decode("utf_8") ,200


@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    
    if payload['password'] == "Vive l'ESIEE !" :
        return jsonify({'token':jwt_utils.build_token()})
    else :
        return '', 401
@app.route('/questions', methods=['POST'])
def addQuestion():
    authorization =  request.headers.get('Authorization')
    if authorization is None :
         return '', 401
    body = request.get_json()
    question =QuestionService.convertJsonToQuestion(body)
    resultRequest = QuestionService.createQuestion(question)
    if resultRequest is None :
         return '', 400
    else :
        return '', 200

    

if __name__ == "__main__":
    app.run(ssl_context='adhoc')