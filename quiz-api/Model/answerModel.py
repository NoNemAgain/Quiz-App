import json
class AnswerModel(object):
        def __init__(self, id, text, isCorrect,positionQuestion):
                self.id =id
                self.text =text
                self.isCorrect =isCorrect
                self.positionQuestion =positionQuestion

        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
