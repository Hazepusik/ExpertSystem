__author__ = 'mart'

import json
from dajaxice.decorators import dajaxice_register
from Classes.models import Answer

@dajaxice_register
def sayhello(request):
    return json.dumps({'message':'Hello World'})

@dajaxice_register
def redact_answer(request, id, value):
    if request.user.is_authenticated():
        current_answer = Answer.objects.get(id=int(id))
        current_answer.name = value
        current_answer.save()
        return json.dumps({})
    else:
        return json.dumps({})


