import simplejson as json


class QuestionModel(object):
        def __init__(self,id, position, title, text, image,idQuiz,possibleAnswers,numCorrect):
                self.id =id
                self.position =position
                self.title = title
                self.text =text
                self.image = image
                self.idQuiz =idQuiz
                self.possibleAnswers = possibleAnswers
                self.numCorrect = numCorrect
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4,ensure_ascii=False)
