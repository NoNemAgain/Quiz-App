import json
class QuestionModel(object):
        def __init__(self,id, position, title, text, image,possibleAnswers):
                self.id =id
                self.position =position
                self.title = title
                self.text =text
                self.image = image
                self.possibleAnswers = possibleAnswers
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
