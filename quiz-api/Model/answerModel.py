class AnswerModel(object):
        def __init__(self, id, text, isCorrect,idQuestion,positionAnswer):
                self.id =id
                self.text =text
                self.isCorrect = isCorrect == 1
                self.idQuestion =idQuestion
                self.positionAnswer =positionAnswer

