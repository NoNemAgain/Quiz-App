import json


class QuizModel(object):
        def __init__(self, id,scores,size):
                self.id =id
                self.scores = scores
                self.size = size

        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
                
