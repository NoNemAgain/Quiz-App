import json


class ResponseParticipationModel(object):
        def __init__(self,id,numResponse,idParticipation):
                self.id =id
                self.numResponse = numResponse
                self.idParticipation = idParticipation
        
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
