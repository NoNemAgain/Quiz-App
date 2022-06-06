import simplejson as json


class QuestionsListModel(object):
        def __init__(self,questions):
                self.questions =questions
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4,ensure_ascii=False)
