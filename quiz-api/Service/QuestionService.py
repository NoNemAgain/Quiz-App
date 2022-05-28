import json
import sqlite3
from asyncio.windows_events import NULL
from collections import namedtuple
from msilib.schema import Error

from flask import Flask, jsonify, request
from Model import answerModel, questionModel
from Utils import DAO, Config, jwt_utils

from Service import AnswerService, QuizService


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

def countQuestion(cursor,idQuiz):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT COUNT() FROM Question WHERE idQuiz= ?",str(idQuiz))
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        count = rows[0][0]
        cursor.execute("commit")
        return count

    except Error:
        raise Exception('Get Number of question by IDQuiz query Failed')

def checkPosQuestionExist(cursor,position):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Question WHERE position = ?", (str(position),))
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        question_Result = rows[0]
        cursor.execute("commit")
        return question_Result
    except Error:
        raise Exception('Checking if position has a question query Failed')

def checkNumberQuestionAbovePos(cursor,position):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Question WHERE position > ?", (str(position),))
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        nbQuestioAbovPos = len(rows)
        cursor.execute("commit")
        return nbQuestioAbovPos
    except Error:
        raise Exception('Checking number of question above query Failed')


def incrementValueQuestionPosSup(cursor,positionQuestion,incrementValue):
    try :
        cursor.execute("begin")
        cursor.execute("Update Question SET position = position + ? WHERE position> ?", (incrementValue,positionQuestion))
        cursor.execute("commit")
        
    except Error:
        raise Exception('Incrementing position sup query Failed')

def incrementValueQuestionBetween(cursor,minusPosition,plusPosition,incrementValue):
    try :
        cursor.execute("begin")
        cursor.execute("Update Question SET position = position + ? WHERE position> ? AND position <?", (incrementValue,minusPosition,plusPosition))
        cursor.execute("commit")
        
    except Error:
        raise Exception('Incrementing position sup query Faile') 
def createQuestion(input_question):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        position = input_question.position

        if checkPosQuestionExist(cursor,str(position)) != 0 :
            incrementValueQuestionPosSup(cursor,str(position-1),'1')        

        cursor.execute("begin")
        cursor.execute("INSERT INTO Question VALUES (? ,?, ?, ?, ? ,?,?)", (input_question.id ,input_question.position, input_question.title, input_question.text,input_question.image,input_question.idQuiz ,input_question.numCorrect))
        cursor.execute("commit")
        AnswerService.addAnswerToDataBase(cursor, input_question ,input_question.id)
        DAO.closeDB(connexion)
        
        return '', 200
    except Error:
        return 400

def getQuestionByPositionWithConnexion (cursor,position):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Question WHERE position = ?", ((str(position),)))
        rows = cursor.fetchall()
        question = rows[0]
        cursor.execute("commit")
        return question
    except Error:
        raise Exception(' Get question by position query Failed')

def getQuestionByPosition(position):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()

        firstResult= getQuestionByPositionWithConnexion (cursor,position)

        question = questionModel.QuestionModel(firstResult[0],firstResult[1], firstResult[2], firstResult[3], firstResult[4],firstResult[5],list(),firstResult[6]) 
        AnswerService.addAnswerToQuestionModel(cursor, question)

        DAO.closeDB(connexion)
        return question
    except Error:
       raise Exception('Get question by position query Failed')

def getIdByPosition(cursor,position):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Question WHERE position = ?",(str(position),))

        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        id = rows[0][0]

        cursor.execute("commit")
        return id
    except Error:
        raise Exception('Get Question by ID  query Failed')
def convertJsonToQuestion(body): 
    try :
        answers = []
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        numCorrect = 0
        idAnswer = AnswerService.lastIdAnswer(cursor)
        idQuiz=QuizService.getQuizId(cursor)
        idQuestion = lastIdQuestion(cursor) +1



        for element in body["possibleAnswers"] :
            idAnswer +=1
            answer = answerModel.AnswerModel(idAnswer, element["text"],element["isCorrect"],NULL,len(answers)+1)
            answers.append(answer) 
            if element["isCorrect"] == True :
               numCorrect= len(answers)
        
        question =questionModel.QuestionModel(idQuestion,int(body["position"]), body["title"], body["text"], body["image"],idQuiz, answers,numCorrect)
        DAO.closeDB(connexion)
        return question
    except Error:
        return NULL

def checkIfPositionAlreadyTook(cursor,oldPosition,newPosition):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Question WHERE position = ?", (str(oldPosition),))
        rows = cursor.fetchall()
        old_question_Title = rows[0][2]
        cursor.execute("SELECT * FROM Question WHERE position = ?", (str(newPosition),))
        rows = cursor.fetchall()
        new_question_Title = rows[0][2]
        cursor.execute("commit")
        return old_question_Title==new_question_Title 
    except Error:
        raise Exception('check If Position Already Took query Failed')



def incrementPositionUpdate(cursor ,oldPosition,wantedPosition):
    try :
        if wantedPosition > oldPosition :
            plus =int(wantedPosition)+1
            incrementValueQuestionBetween(cursor,str(oldPosition),str(plus),-1)
        elif wantedPosition < oldPosition :
            minus = int(wantedPosition)-1
            incrementValueQuestionBetween(cursor,str(minus),str(oldPosition),1)
    except Error:
        raise Exception('increment Position Update Failed')

def updateQuestion(oldPosition,updatedQuestion):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        wantedPosition  =str(updatedQuestion.position)

        if checkPosQuestionExist(cursor,oldPosition) == 0 :
              raise Exception(' Delete query Failed')

        id = str(getQuestionByPositionWithConnexion(cursor,oldPosition)[0])
        checkPosition = checkIfPositionAlreadyTook(cursor,oldPosition,wantedPosition)

        if checkPosition == False:
            idWantedPosition = str(getQuestionByPositionWithConnexion(cursor,wantedPosition)[0])
            AnswerService.changeIDQuestionForAnswer(cursor,idWantedPosition,10000)
            incrementPositionUpdate(cursor ,oldPosition,wantedPosition) 

        cursor.execute("begin")
        cursor.execute("Update Question set position = ? , title= ? , text = ? , image = ? WHERE id = ?", (wantedPosition,updatedQuestion.title,updatedQuestion.text,updatedQuestion.image,id))
        cursor.execute("commit")
        if checkPosition == False:
            AnswerService.deleteAnswerWithIdQuestion(cursor,id)

        AnswerService.updateAnswerWithIdQuestion(cursor,id,updatedQuestion.possibleAnswers)
        if checkPosition == False:
            AnswerService.changeIDQuestionForAnswer(cursor,10000,idWantedPosition)
        DAO.closeDB(connexion)
        return '' ,200
    except Error:
        raise Exception(' update Question query Failed')

def deleteQuestion(position):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        idQuest = str(getQuestionByPosition(position).id)

        cursor.execute("begin")
        cursor.execute("DELETE FROM Question WHERE Position = ?", (str(position),))
        cursor.execute("commit")

        AnswerService.deleteAnswerWithIdQuestion(cursor,idQuest)
        if checkNumberQuestionAbovePos(cursor,position) >0 :
            incrementValueQuestionPosSup(cursor,position,'-1')

        DAO.closeDB(connexion)
        return '' ,204
    except Error:
        raise Exception(' delete Question query Failed')
