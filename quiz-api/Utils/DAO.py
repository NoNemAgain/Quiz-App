import json
import sqlite3
from asyncio.windows_events import NULL
from collections import namedtuple
from msilib.schema import Error

from flask import Flask, jsonify, request
from Model import answerModel, questionModel
from Service import AnswerService

from Utils import Config, jwt_utils


def connexionDB():
    try :
        db_connexion = sqlite3.connect(Config.PATH)
        db_connexion.isolation_level = None
        return db_connexion
    except Error:
        raise Exception('Connexion failed')

def closeDB(Connexion):
    try :
        Connexion.close() 
    except Error:
        raise Exception('Deconnexion failed')
