from asyncio.windows_events import NULL
from msilib.schema import Error
from flask import Flask, jsonify, request
from Model import quizModel
from Utils import Config ,jwt_utils,DAO
from Service import AnswerService,ParticipationService,QuestionService
import json
import sqlite3
from collections import namedtuple



def createQuiz():
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        cursor.execute("begin")
        cursor.execute("INSERT INTO Quiz VALUES (NULL)")
        cursor.execute("commit")
        DAO.closeDB(connexion)
        return '', 200
    except Error:
        raise Exception('Create Quiz Failed')

def getQuiz():
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Quiz LIMIT 1")
        
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        firstResult = rows[0]
    
       
        cursor.execute("commit")
        scores = ParticipationService.getAllScore(cursor)
        size = QuestionService.countQuestion(cursor,1)
        question = quizModel.QuizModel(firstResult[0],scores, size) 

        DAO.closeDB(connexion)
        return question
    except Error:
        raise Exception('Get Quiz Failed')

def getQuizId(cursor):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Quiz ORDER BY ID ASC LIMIT 1")
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        idQuiz = rows[0][0]
        cursor.execute("commit")
        return idQuiz
    except Error:
        raise Exception('Get Quiz Failed')


        
        