from Classes.models import Situation, Question, Answer, Recommendation
from django.template import loader, Context
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
import ast


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

def next_question(request, id):
    situation = Situation.objects.get(id=int(id))
    current_keys = request.POST.keys()
    if 'answers' in current_keys:
        already_answers = ast.literal_eval(request.POST['answers'])
    else:
        already_answers = []
    if 'question' in current_keys:
        already_answers.append(int(request.POST['question']))
    recommendation = situation.getRecommendation(already_answers)
    if recommendation:
        temp = loader.get_template("answer.html")
        cont = RequestContext(request, {'data': recommendation, 'already_answers': already_answers})
        return  HttpResponse(temp.render(cont))
    else:
        already_questions = []
        for element in already_answers:
            already_questions.append(Answer.objects.get(id = element).question.id)
        non_answered = situation.getAllQuestions().exclude(id__in=already_questions)
        if non_answered:
            current_question = non_answered[0]
            c = {'quest': current_question,
                 'scenario':id,
                 'answers': str(already_answers),
                 'ans': current_question.getAllAnswers()}
            c.update(csrf(request))
            return render_to_response('uno_question.html', c)
        else:
            temp = loader.get_template("answer.html")
            cont = RequestContext(request, {'data': None})
            return HttpResponse(temp.render(cont))

def expert_entrance(request):
    if request.user.is_authenticated():
        return redirect('/expert/situations/')
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)

def expert_auth(request):
    if request.user.is_authenticated():
        return redirect('/expert/situations/')
    else:
        username = request.POST['login']
        password = request.POST['passw']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/expert/situations/')

    return redirect('/expert/')

def expert_situations(request):
    if request.user.is_authenticated():
        c = {'scenarios': Situation.objects.all()}
        c.update(csrf(request))
        return  render_to_response("expert_scenarios.html", c)
    else:
        return redirect('/expert/')

def add_situation(request):
    if request.user.is_authenticated():
        if 'description' in request.POST.keys():
            description = request.POST['description']
        else:
            description = ''
        new_situation = Situation.new(request.POST['name'], description)
        return redirect('/expert/situations/'+str(new_situation.id)+'/')
    else:
        return redirect('/expert/')

def redact_situation(request, id):
    if request.user.is_authenticated():
        current_situation = Situation.objects.get(id=id)
        recommendations = current_situation.getAllRecommendations()
        questions = current_situation.getAllQuestions()
        conflicts = []
        for recommendation in recommendations:
            if recommendation.hasConflict():
                conflicts.append(recommendation)
        c = {'recommendations': recommendations, 'questions': questions, 'situation': id, 'conflicts': conflicts, 'conflicted': bool(conflicts)}
        c.update(csrf(request))
        return render_to_response("expert_situation.html", c)
    else:
        return redirect('/expert/')

def redact_question(request, id):
    if request.user.is_authenticated():
        current_question = Question.objects.get(id=id)
        answers = current_question.getAllAnswers()
        c = {'question': current_question, 'answers': answers}
        c.update(csrf(request))
        return render_to_response("expert_question.html", c)
    else:
        return redirect('/expert/')

def delete_answer(request, id):
    if request.user.is_authenticated():
        current_answer = Answer.objects.get(id=int(id))
        current_question = current_answer.question
        current_answer.delete()
        return redirect('/expert/questions/'+str(current_question.id)+'/')
    else:
        return redirect('/expert/')

def delete_question(request, id):
    if request.user.is_authenticated():
        current_question = Question.objects.get(id=int(id))
        current_situation = current_question.situation
        current_question.delete()
        return redirect('/expert/situations/'+str(current_situation.id)+'/')
    else:
        return redirect('/expert/')

def delete_situation(request, id):
    if request.user.is_authenticated():
        current_situation = Situation.objects.get(id=int(id))
        current_situation.delete()
        return redirect('/expert/situations/')
    else:
        return redirect('/expert/')

def add_answer(request):
    if request.user.is_authenticated():
        new_answer = Answer.new(request.POST['name'], Question.objects.get(id=int(request.POST['question'])))
        new_answer.save()
        return redirect('/expert/questions/'+str(request.POST['question'])+'/')
    else:
        return redirect('/expert/')


def add_question(request):
    if request.user.is_authenticated():
        new_question = Question.new(request.POST['name'],Situation.objects.get(id=int(request.POST['situation'])))
        return redirect('/expert/questions/'+str(new_question.id)+'/')
    else:
        return redirect('/expert/')

def add_recommendation(request):
    if request.user.is_authenticated():
        if 'description' in request.POST.keys():
            description = request.POST['description']
        else:
            description = ''
        new_question = Recommendation.new(request.POST['name'],Situation.objects.get(id=int(request.POST['situation'])),description)
        return redirect('/expert/recommendations/'+str(new_question.id)+'/')
    else:
        return redirect('/expert/')

def redact_recommendation(request, id):
    if request.user.is_authenticated():
        current_recommendation = Recommendation.objects.get(id=int(id))
        current_situation = current_recommendation.situation
        current_questions = current_situation.getAllQuestions()
        current_conflicts = current_recommendation.hasConflict()
        answers = current_recommendation.getAnswers()
        if current_conflicts:
            conflict_block = loader.render_to_string('conflict_block.html', {'conflicts': current_conflicts})
        else:
            conflict_block=''
        c = {'recommendation': current_recommendation,
             'questions': current_questions,
             'conflicts': current_conflicts,
             'answers': answers,
             'situation': current_situation.id,
             'conflict_block': conflict_block,
             'conflict': bool(conflict_block)}
        c.update(csrf(request))
        return render_to_response("expert_recommendation.html", c)
    else:
        return redirect('/expert/')

def del_recommendation(request, id):
    if request.user.is_authenticated():
        current_question = Recommendation.objects.get(id=int(id))
        current_situation = current_question.situation
        current_question.delete()
        return redirect('/expert/situations/'+str(current_situation.id)+'/')
    else:
        return redirect('/expert/')

def question_setter(request, id):
    if request.user.is_authenticated():
        current_question = Question.objects.get(id=int(id))
        current_situation = current_question.situation
        current_recommendations = current_situation.getAllRecommendations()
        c = {'recommendations': current_recommendations,
             'question': current_question}
        c.update(csrf(request))
        return render_to_response("expert_question_setter.html", c)
    else:
        return redirect('/expert/')
