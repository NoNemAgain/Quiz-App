import json
import sqlite3
from asyncio.windows_events import NULL
from collections import namedtuple
from msilib.schema import Error

from flask import Flask, jsonify, request
from Model import (answerModel, participationModel, questionModel,
                   responseParticipationModel)
from Utils import DAO, Config, jwt_utils

from Service import (AnswerService, QuestionService, QuizService,
                     ResponseParticipationService)


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
        raise Exception('Get Last ID Participation query Failed')
def createParticipation(inputParticipation):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
       
        cursor.execute("begin")
        cursor.execute("INSERT INTO Participation VALUES (? ,?,? ,?)", (inputParticipation.id,inputParticipation.playerName,inputParticipation.score,inputParticipation.idQuiz))
        cursor.execute("commit")
        
        ResponseParticipationService.addResponseParticipationToDataBase(cursor, inputParticipation,str(inputParticipation.id))

        DAO.closeDB(connexion)
        return inputParticipation.toJSON(), 200
    except Error:
        return 400



def getParticipationById(id):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()

        cursor.execute("begin")
        cursor.execute("SELECT * FROM Participation WHERE id = ?", (str(id),))
        rows = cursor.fetchall()
        firstResult = rows[0]
        cursor.execute("commit")

        participation = participationModel.ParticipationModel(id=firstResult[0],playerName=firstResult[1],score=firstResult[2],idQuiz=firstResult[3],responseParticipation=list())
        ResponseParticipationService.addResponseParticipationToModel(cursor,participation)

        DAO.closeDB(connexion)
        return participation
    except Error:
       raise Exception('Qet Participation By ID failed')


def convertJsonToParticipation(body): 
    try :
        answers =[]
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        id = ResponseParticipationService.lastIdResponseParticipation(cursor)
        idQuiz = str(QuizService.getQuizId(cursor))
        idParticipation= lastIdParticipation(cursor)+1
        score = 0 
        count = 0 

        if len(body["answers"]) != QuestionService.countQuestion(cursor,QuizService.getQuizId(cursor)) :
            raise Exception('Get Id Question query Failed')

        for response in body["answers"] :
            count +=1
            id +=1
            answers.append(responseParticipationModel.ResponseParticipationModel(id,response,idParticipation))  
            if response == QuestionService.getQuestionByPosition(count).numCorrect:
                score+=1
        
        participation =participationModel.ParticipationModel(id=idParticipation,playerName=body["playerName"],score=score,idQuiz=idQuiz,responseParticipation=answers)
        DAO.closeDB(connexion)
        return participation
    except Error:
        raise Exception(' Convert Json to Participation Failed')

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


def takeScore(participation):
    return participation.score  
def getAllScore(cursor):
    try :
        scores = []

        cursor.execute("begin") 
        cursor.execute("SELECT * FROM Participation ")
        rows = cursor.fetchall()
        for participation in rows : 
            participationObject =participationModel.ParticipationModel(id=participation[0],playerName=participation[1],score=participation[2],idQuiz=participation[3],responseParticipation=list())
            ResponseParticipationService.addResponseParticipationToModel(cursor, participationObject)
            scores.append(participationObject)
        cursor.execute("commit")
        
        scores.sort(key=takeScore , reverse= True)
        return scores
    except Error:
       raise Exception('get All scored query Failed')
