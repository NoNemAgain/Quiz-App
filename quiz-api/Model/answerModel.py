import json
class AnswerModel(object):
        def __init__(self, id, text, isCorrect,positionQuestion,positionAnswer):
                self.id =id
                self.text =text
                self.isCorrect = str(isCorrect == 1)
                self.positionQuestion =positionQuestion
                self.positionAnswer =positionAnswer

