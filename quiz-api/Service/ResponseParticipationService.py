import json
import sqlite3
from asyncio.windows_events import NULL
from collections import namedtuple
from msilib.schema import Error

from flask import Flask, jsonify, request
from Model import answerModel, questionModel, responseParticipationModel
from Utils import Config, jwt_utils

from Service import AnswerService


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
        raise Exception('Get last ID participation query Failed')



def addResponseParticipationToDataBase(cursor, inputParticipation,idParticipation):
    try:
        for responseParticipation in inputParticipation.responseParticipation :
            cursor.execute("begin") 
            cursor.execute("INSERT INTO ResponseParticipation VALUES (? ,?, ?)", (responseParticipation.id,responseParticipation.numResponse,responseParticipation.idParticipation))
            cursor.execute("commit")
    except Error:
        raise Exception(' Insert  Response Participation To DataBase query Failed')

def deleteAllResponseParticipation(cursor):
    try :
        cursor.execute("begin")
        cursor.execute("DELETE FROM ResponseParticipation")
        cursor.execute("commit")
    except Error:
        raise Exception('delete All Response Participation Failed')

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
