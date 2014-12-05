# -*- coding: utf-8 -*-
from django.db import models
from datetime import date, datetime


class Situation(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="")

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


class Question(models.Model):
    name = models.CharField(max_length=500)
    situation = models.ForeignKey('Situation')

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


class Condition(models.Model):
    answer = models.ForeignKey('Answer')
    conditionSet = models.ForeignKey('ConditionSet')
    isPositive = models.BooleanField(default=True)


class ConditionSet(models.Model):
    conditionSet = models.ForeignKey('Recommendation')

    def getAllConditions(self):
        return Condition.objects.filter(conditionSet = self)