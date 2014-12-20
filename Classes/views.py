from Classes.models import Situation
from django.template import loader, Context
from django.http import HttpResponse
from django.template import RequestContext

def main(request):
    temp = loader.get_template("index.html")
    cont = RequestContext(request, {})
    return  HttpResponse(temp.render(cont))

def situations(request):
    temp = loader.get_template("scenarios.html")
    cont = RequestContext(request, {'scenarios': Situation.objects.all()})
    return  HttpResponse(temp.render(cont))

def questions(request, id):
    temp = loader.get_template("questions.html")
    situation = Situation.objects.get(id=int(id)).getAllQuestions()
    question_dict = {'questions':[]}
    for item in situation:
        question_dict['questions'].append({'quest': item,
                                           'ans': item.getAllAnswers()})
    cont = RequestContext(request, {'questions': question_dict})
    return  HttpResponse(temp.render(cont))