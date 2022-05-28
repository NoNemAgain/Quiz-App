from asyncio.windows_events import NULL
from msilib.schema import Error
from flask import Flask, jsonify, request
from Model import questionModel ,answerModel ,responseParticipationModel,participationModel
from Utils import Config ,jwt_utils,DAO
from Service import AnswerService ,ResponseParticipationService, QuizService ,QuestionService
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
       raise Exception('Query Failed')


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
        countQuestion = QuestionService.countQuestion(cursor,QuizService.getQuizId(cursor))
        if len(body["answers"]) != countQuestion :
            raise Exception('Get Id Question query Failed')

        for response in body["answers"] :
            count +=1
            id +=1
            answer = responseParticipationModel.ResponseParticipationModel(id,response,idParticipation)
            answers.append(answer)  
            if response == QuestionService.getQuestionByPosition(count).numCorrect:
                score+=1
        
        participation =participationModel.ParticipationModel(id=idParticipation,playerName=body["playerName"],score=score,idQuiz=idQuiz,responseParticipation=answers)
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

def getAllScore(cursor):
    try :
        scores = []
        cursor.execute("begin") 
        cursor.execute("SELECT * FROM Participation ")
        rows = cursor.fetchall()
        for participation in rows : 
            scores.append(participation)
        cursor.execute("commit")
        return scores
    except Error:
       raise Exception('Query Failed')