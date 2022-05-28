import json


class ParticipationModel(object):
        def __init__(self,id,playerName,score,idQuiz,responseParticipation):
                self.id =id
                self.playerName=playerName
                self.score=score
                self.idQuiz=idQuiz
                self.responseParticipation= responseParticipation
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
