from Classes.models import Situation
from django.template import loader, Context
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

def main(request):
    temp = loader.get_template("index.html")
    cont = RequestContext(request, {})
    return  HttpResponse(temp.render(cont))

def situations(request):
    temp = loader.get_template("scenarios.html")
    cont = RequestContext(request, {'scenarios': Situation.objects.all()})
    return  HttpResponse(temp.render(cont))

def questions(request, id):
    situation = Situation.objects.get(id=int(id)).getAllQuestions()
    question_dict = []
    for item in situation:
        question_dict.append({'quest': item,
                                           'ans': item.getAllAnswers()})
    c = {'questions': question_dict, 'scenario':id}
    c.update(csrf(request))
    return render_to_response('questions.html', c)

def solution(request):
    situation = Situation.objects.get(id=int(request.POST['sit']))
    allq = situation.getAllQuestions()
    answers = []
    list_of_answered = request.POST.keys()
    for question in allq:
        if 'q'+str(question.id) in list_of_answered:
            current_answer = request.POST['q'+str(question.id)]
            answers.append(int(current_answer))
    recomm = situation.getRecommendation(answers)
    temp = loader.get_template("answer.html")
    c = {'data': recomm}
    c.update(csrf(request))
    cont = RequestContext(request, {'data': recomm})
    return  HttpResponse(temp.render(cont))
