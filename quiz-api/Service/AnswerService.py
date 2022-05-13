from asyncio.windows_events import NULL
from msilib.schema import Error
from flask import Flask, jsonify, request
from Model import questionModel ,answerModel
from Utils import Config ,jwt_utils
import json
import sqlite3
from collections import namedtuple



def addAnswerToQuestion(cursor, questions):
    try :
        answers = []
        cursor.execute("begin")
        insertion_result = cursor.execute("SELECT * FROM Answer")
        rows = cursor.fetchall()

        for elem in rows:
           answers.append(answerModel.AnswerModel(elem[0],elem[1],elem[2],elem[3]))
        cursor.execute("commit")

        
        for question in questions :
            for answer in answers:
                if question.position == answer.positionQuestion :
                    question.possibleAnswers.append(answer)
        return answers
    except Error:
        return NULL




    