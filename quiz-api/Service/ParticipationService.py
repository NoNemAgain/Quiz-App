from asyncio.windows_events import NULL
from msilib.schema import Error
from flask import Flask, jsonify, request
from Model import questionModel ,answerModel ,responseParticipationModel,participationModel
from Utils import Config ,jwt_utils,DAO
from Service import AnswerService ,ResponseParticipationService, QuizService
import json
import sqlite3
from collections import namedtuple
def lastIdParticipation(cursor):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Participation ORDER BY ID DESC LIMIT 1")
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        lastId = rows[0][0]
        cursor.execute("commit")
        return lastId

    except Error:
        raise Exception('Get Id Question query Failed')
def createParticipation(inputParticipation):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        idQuiz = QuizService.getQuizId(cursor)
        idParticipation= lastIdParticipation(cursor)
        cursor.execute("begin")
        cursor.execute("INSERT INTO Participation VALUES (? ,?,NULL,?)", (idParticipation,inputParticipation.playerName,idQuiz))
        cursor.execute("commit")
        ResponseParticipationService.addResponseParticipationToDataBase(cursor, inputParticipation,idParticipation)
        DAO.closeDB(connexion)
        return '', 200
    except Error:
        return 400

def convertJsonToQuestion(body): 
    try :
        answers =[]
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        id = ResponseParticipationService.lastIdResponseParticipation(cursor)
        idParticipation = lastIdParticipation(connexion.cursor())+1
        for element in body["answers"] :
            id +=1
            answer = responseParticipationModel.ResponseParticipationModel(id,element,idParticipation)
            answers.append(answer) 
        
        participation =participationModel.ParticipationModel(id=idParticipation,playerName=body["playerName"],score=NULL,idQuiz=QuizService.getQuizId(cursor),responseParticipation=answers)
        DAO.closeDB(connexion)
        return participation
    except Error:
        return NULL

def deleteAllParticipiation():
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        ResponseParticipationService.deleteAllResponseParticipation(cursor)
        cursor.execute("begin")
        cursor.execute("DELETE FROM Participation")
        cursor.execute("commit")
        DAO.closeDB(connexion)
        return '' ,204
    except Error:
        raise Exception(' Delete query Failed')