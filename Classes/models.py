# -*- coding: utf-8 -*-
from django.db import models
from datetime import date, datetime
from django.template import loader, Context
from django.http import HttpResponse
from django.template import RequestContext


class Situation(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="")

    @staticmethod
    def new(_name, _descr = ""):
        s = Situation()
        s.name = _name
        s.description = _descr
        s.save()
        return s

    def addQuestion(self, question):
        question.situation = self
        question.save()

    def addQuestions(self, questions):
        for question in questions:
            self.addQuestion(question)

    def getAllQuestions(self):
        questions = Question.objects.filter(situation=self)
        return questions

    def getAllRecommendations(self):
        recommendation = Recommendation.objects.filter(situation=self)
        return recommendation

    def getRecommendation(self, answerIds):
        answerIds = set(answerIds)
        for rec in self.getAllRecommendations():
            conditions = ConditionSet.filter(recommendation = rec)
            for c in conditions:
                cAnsIds = []
                for condition in c.getAllConditions():
                    cAnsIds.append(condition.answer.id)
                cAnsIds = set(cAnsIds)
                if cAnsIds.issubset(answerIds):
                    return rec
        return None

    def hasConflict(self, answerIds):
        conflictWith = []
        answerIds = set(answerIds)
        for rec in self.getAllRecommendations():
            conditions = ConditionSet.filter(recommendation = rec)
            for c in conditions:
                cAnsIds = []
                for condition in c.getAllConditions():
                    cAnsIds.append(condition.answer.id)
                cAnsIds = set(cAnsIds)
                if answerIds.issubset(cAnsIds):
                    conflictWith.append(rec)
        return conflictWith

class Recommendation(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="")
    situation = models.ForeignKey('Situation')

    @staticmethod
    def new(_name, _sit, _descr = ""):
        r = Recommendation()
        r.name = _name
        r.description = _descr
        r.situation = _sit
        r.save()
        return r


class Question(models.Model):
    name = models.CharField(max_length=500)
    situation = models.ForeignKey('Situation')

    @staticmethod
    def new(_name, _sit):
        q = Question()
        q.name = _name
        q.situation = _sit
        q.save()
        return q

    def getAllAnswers(self):
        answers = Answer.objects.filter(question=self)
        return answers

    def addAnswer(self, answer):
        answer.question = self
        answer.save()

    def addAnswers(self, answers):
        for answer in answers:
            self.addAnswer(answer)


class Answer(models.Model):
    name = models.CharField(max_length=500)
    question = models.ForeignKey('Question')

    @staticmethod
    def new(_name, _q):
        a = Answer()
        a.name = _name
        a.question = _q
        a.save()
        return a

class Condition(models.Model):
    answer = models.ForeignKey('Answer')
    conditionSet = models.ForeignKey('ConditionSet')
    isPositive = models.BooleanField(default=True)

    @staticmethod
    def new(_a, _cs, _ip=True):
        c = Condition()
        c.answer = _a
        c.conditionSet = _cs
        c.isPositive = _ip
        c.save()
        return c

class ConditionSet(models.Model):
    recommendation = models.ForeignKey('Recommendation')

    @staticmethod
    def new(_r):
        cs = ConditionSet()
        cs.recommendation = _r
        return cs

    def getAllConditions(self):
        return Condition.objects.filter(conditionSet = self)


def test(request):
    temp = loader.get_template("test.html")
    s = Situation.new('qqq', 'www')
    r = Recommendation()
    r.name = 'fuck yourself'
    r.situation = s
    r.save()
    q = Question()
    q.name = '?'
    q.situation = s
    q.save()
    a = Answer()
    a.name = 'loool'
    a.question = q
    a.save()
    alt_a = Answer()
    alt_a.name = 'foo bar'
    alt_a.question = q
    alt_a.save()
    cont = RequestContext(request, {'data': s.name})
    return  HttpResponse(temp.render(cont))