import json
class QuizModel(object):
        def __init__(self, id,size,scores):
                self.id =id
                self.size = size
                self.scores = scores
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
                
