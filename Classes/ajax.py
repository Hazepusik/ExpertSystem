__author__ = 'mart'

import json
from dajaxice.decorators import dajaxice_register
from Classes.models import Answer, Recommendation, Question
from django.template import loader
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


@dajaxice_register
def redact_condition(request, recommendation_id, answer_id, question_id):
    if request.user.is_authenticated():
        current_recommendation = Recommendation.objects.get(id=int(recommendation_id))
        if answer_id == '-1':
            current_recommendation.delAnswer(Question.objects.get(id=int(question_id)))
        else:
            current_recommendation.addAnswer(Answer.objects.get(id=int(answer_id)))
        current_conflicts = current_recommendation.hasConflict()
        if current_conflicts:
            conflict_block = loader.render_to_string('conflict_block.html', {'conflicts': current_conflicts})
        else:
            conflict_block=''
        return json.dumps({'message':conflict_block})
    else:
        return json.dumps({})

