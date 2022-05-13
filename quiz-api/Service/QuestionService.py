from flask import Flask, jsonify, request
from flask import Flask, jsonify, request
from Model import questionModel
from Utils import Config ,jwt_utils
import json
import sqlite3
from collections import namedtuple

def connectionDB():
    db_connection = sqlite3.connect(Config.PATH)
    db_connection.isolation_level = None
    return db_connection


def createQuestion(input_question):
    db_connection = connectionDB()
    cur = db_connection.cursor()
    # start transaction
    cur.execute("begin")

    # save the question to db
    insertion_result = cur.execute(f"insert into Question (title,text,image) values"
    f"('{input_question.title, input_question.text, input_question.image}')")

    #send the request
    cur.execute("commit")

def convertQuestionToJson(question): 
    return json.dumps(question.__dict__)



# def customQuestionDecoder(questionInput):
#     return namedtuple(Question, questionInput.keys())(*questionInput.values())
def convertJsonToQuestion(body): 
    question = questionModel.QuestionModel(int(body["position"]), body["title"], body["text"], body["image"])
    return question


    