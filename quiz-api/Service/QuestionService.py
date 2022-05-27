from asyncio.windows_events import NULL
from msilib.schema import Error
from flask import Flask, jsonify, request
from Model import questionModel ,answerModel
from Utils import Config ,jwt_utils,DAO
from Service import AnswerService,QuizService
import json
import sqlite3
from collections import namedtuple

def lastIdQuestion(cursor):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Question ORDER BY ID DESC LIMIT 1")
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        lastId = rows[0][0]
        cursor.execute("commit")
        return lastId

    except Error:
        raise Exception('Get Id Question query Failed')

def checkPosQuestionExist(cursor,position):
    cursor.execute("begin")
    cursor.execute("SELECT * FROM Question WHERE position = ?", (position))
    rows = cursor.fetchall()
    if len(rows) ==0  :
        cursor.execute("commit")
        return 0
    question_Result = rows[0]
    cursor.execute("commit")
    return question_Result

def checkNumberQuestionAbovePos(cursor,position):
    cursor.execute("begin")
    cursor.execute("SELECT * FROM Question WHERE position > ?", (position))
    rows = cursor.fetchall()
    if len(rows) ==0  :
        cursor.execute("commit")
        return 0
    nbQuestioAbovPos = len(rows)
    cursor.execute("commit")
    return nbQuestioAbovPos


def incrementValueQuestionPosSup(cursor,positionQuestion,incrementValue):
    try :
        cursor.execute("begin")
        cursor.execute("Update Question SET position = position + ? WHERE position> ?", (incrementValue,positionQuestion))
        cursor.execute("commit")
        
    except Error:
        raise Exception('Adding answer query Failed')   

def createQuestion(input_question):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        #Check if position already taken 
        position = input_question.position

        checkPos =checkPosQuestionExist(cursor,str(position))
        if checkPos != 0 :
            incrementValueQuestionPosSup(cursor,str(position-1),'1')        
        idQuestion = lastIdQuestion(cursor) +1
        idQuiz = QuizService.getQuizId(cursor)
        cursor.execute("begin")
        cursor.execute("INSERT INTO Question VALUES (? ,?, ?, ?, ? ,?)", (idQuestion ,input_question.position, input_question.title, input_question.text,input_question.image,idQuiz ))
        cursor.execute("commit")
        AnswerService.addAnswerToDataBase(cursor, input_question ,idQuestion)
        DAO.closeDB(connexion)
        return '', 200
    except Error:
        return 400

def getQuestionByPosition(position):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Question where position = ? ", (position))
        rows = cursor.fetchall()
        firstResult = rows[0]
        question = questionModel.QuestionModel(firstResult[0],firstResult[1], firstResult[2], firstResult[3], firstResult[4], list()) 
        cursor.execute("commit")
        AnswerService.addAnswerToQuestionModel(cursor, question)
        DAO.closeDB(connexion)
        return question
    except Error:
       raise Exception('Query Failed')


def convertJsonToQuestion(body): 
    try :
        answers = []
        posQuestion = int(body["position"])
        connexion = DAO.connexionDB()
       
        id = AnswerService.lastIdAnswer(connexion.cursor())
        for element in body["possibleAnswers"] :
            id +=1
            answer = answerModel.AnswerModel(id, element["text"],element["isCorrect"],posQuestion,len(answers)+1)
            answers.append(answer) 
        id = lastIdQuestion(connexion.cursor())+1
        question =questionModel.QuestionModel(id,posQuestion, body["title"], body["text"], body["image"], answers)
        DAO.closeDB(connexion)
        return question
    except Error:
        return NULL

def updateQuestion(oldIdQuestion,updatedQuestion):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        if checkPosQuestionExist(cursor,oldIdQuestion) == 0 :
              raise Exception(' Delete query Failed')
        cursor.execute("begin")
        cursor.execute("Update Question set position = ? , title= ? , text = ? , image = ? WHERE Position = ?", (updatedQuestion.position,updatedQuestion.title,updatedQuestion.text,updatedQuestion.image,oldIdQuestion))
        cursor.execute("commit")
        AnswerService.updateAnswerWithIdQuestion(cursor,oldIdQuestion,updatedQuestion.possibleAnswers)
        DAO.closeDB(connexion)
        return '' ,200
    except Error:
        raise Exception(' Delete query Failed')

def deleteQuestion(position):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        idQuest = str(getQuestionByPosition(position).id)
        cursor.execute("begin")
        cursor.execute("DELETE FROM Question WHERE Position = ?", (position))
        cursor.execute("commit")
        AnswerService.deleteAnswerWithIdQuestion(cursor,idQuest)
        if checkNumberQuestionAbovePos(cursor,position) >0 :
            incrementValueQuestionPosSup(cursor,position,'-1')
        DAO.closeDB(connexion)
        return '' ,204
    except Error:
        raise Exception(' Delete query Failed')

    