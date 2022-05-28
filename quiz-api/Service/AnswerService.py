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
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Answer ORDER BY ID DESC LIMIT 1")
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        lastId = rows[0][0]
        cursor.execute("commit")
        return lastId

    except Error:
        raise Exception('Get Id Answer query Failed')


def addAnswerToQuestionModel(cursor, question):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Answer where idQuestion = ?",(str(question.id),))
        rows = cursor.fetchall()
        for elem in rows:
           question.possibleAnswers.append(answerModel.AnswerModel(elem[0],elem[1],elem[2],elem[3],elem[4]))
        cursor.execute("commit")
    except Error:
        raise Exception('Adding answer query Failed')

def checkIfQuestionHasAlreadyHisAnswer(cursor,idQuestion):
    try : 
        cursor.execute("begin") 
        cursor.execute("SELECT * FROM Answer where idQuestion = ?", (idQuestion,))
        rows = cursor.fetchall()
        if rows[0][1] == 4 :
            raise Exception('Only 4 answers are allowed ')

        cursor.execute("commit")
    except Error:
        pass
def addAnswerToDataBase(cursor, input_question,idQuestion):
    try:
        for answer in input_question.possibleAnswers :
            cursor.execute("begin") 
            cursor.execute("INSERT INTO Answer VALUES (? ,?, ?, ?, ?)", (answer.id, answer.text, answer.isCorrect,idQuestion,answer.positionAnswer))
            cursor.execute("commit")
    except Error:
        raise Exception(' Insert  Answer query Failed')

def deleteAnswerWithIdQuestion(cursor,idQuestion):
    try:
        cursor.execute("begin")
        cursor.execute("DELETE FROM Answer where idQuestion = ?", (idQuestion,))
        cursor.execute("commit")
    except Error:
        raise Exception(' Delete Answer query Failed')
    

def updateAnswerWithIdQuestion(cursor,oldIdQuestion,possibleAnswers):
    deleteAnswerWithIdQuestion(cursor,oldIdQuestion)
    for possibleAnswer in possibleAnswers :
        cursor.execute("begin")
        cursor.execute("INSERT INTO Answer VALUES (? ,?, ?, ?, ?)", (possibleAnswer.id,possibleAnswer.text,possibleAnswer.isCorrect,oldIdQuestion,possibleAnswer.positionAnswer))
        cursor.execute("commit")

def changeIDQuestionForAnswer(cursor,oldIdQuestion,wantedId):
    try :
        cursor.execute("begin")
        cursor.execute("Update Answer set idQuestion = ? where idQuestion = ?",(str(wantedId),str(oldIdQuestion)))
        cursor.execute("commit")
    except Error:
        raise Exception('Adding answer query Failed')



def incrementAnswerPosSup(cursor,position):
    try :
        cursor.execute("begin")
        cursor.execute("Update Answer SET idQuestion = idQuestion +1 WHERE idQuestion>= ?", (position))
        cursor.execute("commit")
        
    except Error:
        raise Exception('Adding answer query Failed')