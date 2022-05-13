from asyncio.windows_events import NULL
from msilib.schema import Error
from flask import Flask, jsonify, request
from Model import questionModel ,answerModel
from Utils import Config ,jwt_utils
import json
import sqlite3
from collections import namedtuple

def connectionDB():
    db_connection = sqlite3.connect(Config.PATH)
    db_connection.isolation_level = None
    cursor = db_connection.cursor()
    return cursor


def createQuestion(input_question):
    try :
        cursor = connectionDB()
        cursor.execute("begin")
        for answer in input_question.possibleAnswers :
            cursor.execute("INSERT INTO Answer VALUES (?, ?, ?, ?)", (answer.id, answer.text, answer.isCorrect,answer.positionQuestion ))
        insertion_result = cursor.execute("INSERT INTO Question VALUES (?, ?, ?, ?)", (input_question.position, input_question.title, input_question.text,input_question.image))
        cursor.execute("commit")
        return insertion_result
    except Error:
        return NULL

def getQuestionByPosition(position):
    try :
        answers = []
        cursor = connectionDB()
        cursor.execute("begin")
        insertion_result = cursor.execute("SELECT * FROM Answer")
        rows = cursor.fetchall()

        for elem in rows:
           answers.append(answerModel.AnswerModel(elem[0],elem[1],elem[2],elem[3])) 

        cursor.execute("commit")
        return answers
    except Error:
        return NULL


def convertQuestionToJson(question): 
    return question[0].toJSON()

def convertJsonToQuestion(body): 
    try :
        answers = []
        posQuestion = int(body["position"])
        for element in body["possibleAnswers"] :
            answer = answerModel.AnswerModel(len(answers)+1, element["text"],element["isCorrect"],posQuestion)
            answers.append(answer)
        question =questionModel.QuestionModel(posQuestion, body["title"], body["text"], body["image"], answers)
        return question
    except Error:
        return NULL


    