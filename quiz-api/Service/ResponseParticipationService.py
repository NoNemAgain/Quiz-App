from asyncio.windows_events import NULL
from msilib.schema import Error
from flask import Flask, jsonify, request
from Model import questionModel ,answerModel,responseParticipationModel
from Utils import Config ,jwt_utils
from Service import AnswerService
import json
import sqlite3
from collections import namedtuple

def lastIdResponseParticipation(cursor):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM ResponseParticipation ORDER BY ID DESC LIMIT 1")
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        lastId = rows[0][0]
        cursor.execute("commit")
        return lastId

    except Error:
        raise Exception('Get Id Question query Failed')



def addResponseParticipationToDataBase(cursor, inputParticipation,idParticipation):
    try:
        for responseParticipation in inputParticipation.responseParticipation :
            cursor.execute("begin") 
            cursor.execute("INSERT INTO ResponseParticipation VALUES (? ,?, ?)", (responseParticipation.id,responseParticipation.numResponse,responseParticipation.idParticipation))
            cursor.execute("commit")
    except Error:
        raise Exception(' Insert  Answer query Failed')

def deleteAllResponseParticipation(cursor):
    try :
        cursor.execute("begin")
        cursor.execute("DELETE FROM ResponseParticipation")
        cursor.execute("commit")
    except Error:
        raise Exception(' Delete query Failed')

def addResponseParticipationToModel(cursor, participation):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM ResponseParticipation where idParticipation = ?",(str(participation.id),))
        rows = cursor.fetchall()
        for rp in rows:
           participation.responseParticipation.append(responseParticipationModel.ResponseParticipationModel(id=rp[0],numResponse=rp[1],idParticipation=rp[2]))
        cursor.execute("commit")
    except Error:
        raise Exception('Adding answer query Failed')