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
    cursor.execute("SELECT * FROM Question WHERE position = ?", (str(position)))
    rows = cursor.fetchall()
    if len(rows) ==0  :
        cursor.execute("commit")
        return 0
    question_Result = rows[0]
    cursor.execute("commit")
    return question_Result

def checkNumberQuestionAbovePos(cursor,position):
    cursor.execute("begin")
    cursor.execute("SELECT * FROM Question WHERE position > ?", (str(position)))
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

def incrementValueQuestionBetween(cursor,minusPosition,plusPosition,incrementValue):
    try :
        cursor.execute("begin")
        cursor.execute("Update Question SET position = position + ? WHERE position> ? AND position <?", (incrementValue,minusPosition,plusPosition))
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

def getQuestionByPositionWithConnexion (cursor,position):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Question WHERE position = ?", (str(position)))
        rows = cursor.fetchall()
        question = rows[0]
        cursor.execute("commit")
        return question
    except Error:
        raise Exception(' Delete query Failed')

def getQuestionByPosition(position):
    try :
        connexion = DAO.connexionDB()
        cursor = connexion.cursor()
        firstResult= getQuestionByPositionWithConnexion (cursor,position)
        question = questionModel.QuestionModel(firstResult[0],firstResult[1], firstResult[2], firstResult[3], firstResult[4], list()) 
        AnswerService.addAnswerToQuestionModel(cursor, question)
        DAO.closeDB(connexion)
        return question
    except Error:
       raise Exception('Query Failed')

def getIdByPosition(cursor,position):
    try :
        cursor.execute("begin")
        cursor.execute("SELECT * FROM Question WHERE position = ?",position)
        rows = cursor.fetchall()
        if len(rows) ==0  :
            cursor.execute("commit")
            return 0
        id = rows[0][0]
        cursor.execute("commit")
        return id
    except Error:
        raise Exception('Get Id Question query Failed')
def convertJsonToQuestion(body): 
    try :
        answers = []
        posQuestion = int(body["position"])
        connexion = DAO.connexionDB()
       
        idAnswer = AnswerService.lastIdAnswer(connexion.cursor())
        # idQuestion = lastIdQuestion(connexion.cursor())+1
        idQuestion = lastIdQuestion(connexion.cursor())
        for element in body["possibleAnswers"] :
            idAnswer +=1
            answer = answerModel.AnswerModel(idAnswer, element["text"],element["isCorrect"],idQuestion,len(answers)+1)
            answers.append(answer) 
        
        question =questionModel.QuestionModel(idQuestion,posQuestion, body["title"], body["text"], body["image"], answers)
        DAO.closeDB(connexion)
        return question
    except Error:
        return NULL

def checkIfPositionAlreadyTook(cursor,oldPosition,newPosition):
    cursor.execute("begin")
    cursor.execute("SELECT * FROM Question WHERE position = ?", (oldPosition))
    rows = cursor.fetchall()
    old_question_Title = rows[0][2]
    cursor.execute("commit")
    cursor.execute("begin")
    cursor.execute("SELECT * FROM Question WHERE position = ?", (str(newPosition)))
    rows = cursor.fetchall()
    new_question_Title = rows[0][2]
    cursor.execute("commit")
    return old_question_Title==new_question_Title 



def incrementPositionUpdate(cursor ,oldPosition,wantedPosition):
    

    if wantedPosition > oldPosition :
        minus = int(oldPosition)-1
        incrementValueQuestionBetween(cursor,str(minus),str(wantedPosition),-1)
    elif wantedPosition < oldPosition :
        minus = int(wantedPosition)-1
        incrementValueQuestionBetween(cursor,str(minus),str(oldPosition),1)

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
            AnswerService.changeIDQuestionForAnswer(cursor,wantedPosition,10000)
            incrementPositionUpdate(cursor ,oldPosition,wantedPosition) 

        cursor.execute("begin")
        cursor.execute("Update Question set position = ? , title= ? , text = ? , image = ? WHERE id = ?", (wantedPosition,updatedQuestion.title,updatedQuestion.text,updatedQuestion.image,id))
        cursor.execute("commit")
        if checkPosition == False:
           
            AnswerService.deleteAnswerWithIdQuestion(cursor,id)

        AnswerService.updateAnswerWithIdQuestion(cursor,id,updatedQuestion.possibleAnswers)
        # if checkPosition == False:
        #     AnswerService.changeIDQuestionForAnswer(cursor,10000,oldID)
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

    