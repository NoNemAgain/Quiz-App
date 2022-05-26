import json
class ParticipationModel(object):
        def __init__(self,id,playerName,score,idQuiz):
                self.id =id
                self.playerName=playerName
                self.score=score
                self.idQuiz=idQuiz
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
