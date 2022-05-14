from asyncio.windows_events import NULL
from msilib.schema import Error
from flask import Flask, jsonify, request
from Model import questionModel ,answerModel
from Utils import Config ,jwt_utils
from Service import AnswerService
import json
import sqlite3
from collections import namedtuple



def checkPosQuestionExist(cursor):
    try :
        cursor.execute("begin")
        request_result = cursor.execute("SELECT * FROM Question ORDER BY POSITION DESC LIMIT 1")
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return NULL
        question_Result = rows[0]
        cursor.execute("commit")
        return question_Result

    except Error:
        raise Exception('Adding answer query Failed')

def connectionDB():
    db_connection = sqlite3.connect(Config.PATH)
    db_connection.isolation_level = None
    cursor = db_connection.cursor()
    return cursor

def createQuestion(input_question):
    try :
        cursor = connectionDB()
        #Check if position already taken 
        #Increment other posQuestion + 1 of question
        #Increment answer posQuestion+1 
        cursor.execute("begin")
        request_result = cursor.execute("INSERT INTO Question VALUES (?, ?, ?, ?)", (input_question.position, input_question.title, input_question.text,input_question.image))
        cursor.execute("commit")
        AnswerService.addAnswerToDataBase(cursor, input_question)
        return '', 200
    except Error:
        return 400

def getQuestionByPosition(position):
    try :
        questions = []
        cursor = connectionDB()
        cursor.execute("begin")
        request_result = cursor.execute("SELECT * FROM Question where position = ?", (position))
        rows = cursor.fetchall()

        for element in rows:
            question = questionModel.QuestionModel(element[0], element[1], element[2], element[3], list()) 
            questions.append(question)
        cursor.execute("commit")

        answers = AnswerService.addAnswerToQuestion(cursor, questions)
       
        return questions
    except Error:
       raise Exception('Query Failed')


def convertQuestionToJson(question): 
        try :
            return question[0].toJSON()
        except Error:
            raise Exception(' Convert to Json Failed')

def convertJsonToQuestion(body): 
    try :
        answers = []
        posQuestion = int(body["position"])
        
        id = AnswerService.lastIdAnswer(connectionDB())
        for element in body["possibleAnswers"] :
            id +=1
            answer = answerModel.AnswerModel(id, element["text"],element["isCorrect"],posQuestion,len(answers)+1)
            answers.append(answer) 
        question =questionModel.QuestionModel(posQuestion, body["title"], body["text"], body["image"], answers)
        return question
    except Error:
        return NULL

def updateQuestion(oldPositionQuestion,updatedQuestion):
    try :
        cursor = connectionDB()
        if checkPosQuestionExist(cursor) == NULL :
              raise Exception(' Delete query Failed')
        cursor.execute("begin")
        request_result = cursor.execute("Update Question set position = ? , title= ? , text = ? , image = ? WHERE Position = ?", (updatedQuestion.position,updatedQuestion.title,updatedQuestion.text,updatedQuestion.image,oldPositionQuestion))
        cursor.execute("commit")
        AnswerService.updateAnswerWithPositionQuestion(connectionDB(),oldPositionQuestion,updatedQuestion.possibleAnswers)
        return '' ,200
    except Error:
        raise Exception(' Delete query Failed')

def deleteQuestion(positionQuestion):
    try :
        cursor = connectionDB()
        cursor.execute("begin")
        request_result = cursor.execute("DELETE FROM Question WHERE Position = ?", (positionQuestion))
        cursor.execute("commit")
        AnswerService.deleteAnswerWithPositionQuestion(cursor,positionQuestion)
        return '' ,204
    except Error:
        raise Exception(' Delete query Failed')

    