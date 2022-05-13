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

    cur.execute("begin")

    insertion_result = cur.execute("INSERT INTO Question VALUES (?, ?, ?, ?)", (input_question.position, input_question.title, input_question.text,input_question.image))

    cur.execute("commit")

   

def convertQuestionToJson(question): 
    return json.dumps(question.__dict__)

def convertJsonToQuestion(body): 
    question = questionModel.QuestionModel(int(body["position"]), body["title"], body["text"], body["image"])
    return question


    