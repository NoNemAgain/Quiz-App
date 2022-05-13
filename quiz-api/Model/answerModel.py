import json
class AnswerModel(object):
        def __init__(self, id, text, isCorrect,positionQuestion):
                self.id =id
                self.text =text
                self.isCorrect = isCorrect == 1
                self.positionQuestion =positionQuestion

