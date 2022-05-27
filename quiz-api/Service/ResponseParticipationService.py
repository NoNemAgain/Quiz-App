from asyncio.windows_events import NULL
from msilib.schema import Error
from flask import Flask, jsonify, request
from Model import questionModel ,answerModel
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