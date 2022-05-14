from asyncio.windows_events import NULL
from distutils.log import error
from msilib.schema import Error
from flask import Flask, jsonify, request
from Model import questionModel ,answerModel
from Utils import Config ,jwt_utils
import json
import sqlite3
from collections import namedtuple
from Service import QuestionService

def lastIdAnswer(cursor):
    cursor.execute("begin")
    request_result = cursor.execute("SELECT * FROM Answer ORDER BY ID DESC LIMIT 1")
    rows = cursor.fetchall()
    lastId = rows[0][0]
    cursor.execute("commit")
    return lastId

def addAnswerToQuestion(cursor, questions):
    try :
        answers = []
        cursor.execute("begin")
        request_result = cursor.execute("SELECT * FROM Answer")
        rows = cursor.fetchall()
        for elem in rows:
           answers.append(answerModel.AnswerModel(elem[0],elem[1],elem[2],elem[3],elem[4]))
        cursor.execute("commit")
        for question in questions :
            for answer in answers:
                if question.position == answer.positionQuestion :
                    question.possibleAnswers.append(answer)
        return answers
    except Error:
        raise Exception('Adding answer query Failed')

def addAnswerToDataBase(cursor, input_question):
    try:
        id = lastIdAnswer(cursor)
        for answer in input_question.possibleAnswers :
            cursor.execute("begin") 
            id +=1 
            cursor.execute("INSERT INTO Answer VALUES (? ,?, ?, ?, ?)", (id, answer.text, answer.isCorrect,answer.positionQuestion,answer.positionAnswer ))

            cursor.execute("commit")
    except Error:
        raise Exception(' Insert  Answer query Failed')

def deleteAnswerWithPositionQuestion(cursor,positionQuestion):
    try:
        cursor.execute("begin")
        request_result = cursor.execute("DELETE FROM Answer where PositionQuestion = ?", (positionQuestion))
        cursor.execute("commit")
    except Error:
        raise Exception(' Delete Answer query Failed')
    

def updateAnswerWithPositionQuestion(cursor,positionQuestion,possibleAnswers):
    pass
    # for possibleAnswer in possibleAnswers :
    #     cursor.execute("begin")
    #     request_result = cursor.execute("Update Answer set position = ? , title= ? , text = ? , image = ? WHERE Position = ?", (updatedQuestion.position,updatedQuestion.title,updatedQuestion.text,updatedQuestion.image,oldPositionQuestion))
    #     cursor.execute("commit")
    