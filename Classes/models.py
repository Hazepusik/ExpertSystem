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
            conditions = ConditionSet.objects.filter(recommendation = rec)
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
            conditions = ConditionSet.objects.filter(recommendation = rec)
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
        cs.save()
        return cs

    def getAllConditions(self):
        return Condition.objects.filter(conditionSet = self)


def test(request):
    temp = loader.get_template("test.html")
    s = Situation.new('qqq', 'www')
    r1 = Recommendation.new('rec a1_1, a2_2', s)
    r2 = Recommendation.new('rec a1_2, a2_1', s)
    r3 = Recommendation.new('rec a1_1', s)
    q1 = Question.new('q2?', s)
    a1_1 = Answer.new('a1_1', q1)
    a1_2 = Answer.new('a1_2', q1)

    q2 = Question.new('q1?', s)
    a2_1 = Answer.new('a2_1', q2)
    a2_2 = Answer.new('a2_2', q2)

    q3 = Question.new('q3?', s)

    cs1 = ConditionSet().new(r1)
    c1_1 = Condition().new(a1_1, cs1)
    c2_2 = Condition().new(a2_2, cs1)

    cs2 = ConditionSet().new(r2)
    c2_1 = Condition().new(a2_1, cs2)
    c2_1 = Condition().new(a1_2, cs2)

    cs3 = ConditionSet().new(r3)
    c3_1 = Condition().new(a1_1, cs3)


    cont = RequestContext(request, {'data': s.hasConflict([a1_1.id])})
    return  HttpResponse(temp.render(cont))