# -*- coding: utf-8 -*-
from django.db import models
from datetime import date, datetime


class Situation(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="")


class Recommendation(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="")


class Question(models.Model):
    name = models.CharField(max_length=500)
    situation = models.ForeignKey('Situation')


class Answer(models.Model):
    name = models.CharField(max_length=500)
    question = models.ForeignKey('Question')


class Condition(models.Model):
    answer = models.ForeignKey('Answer')
    conditionSet = models.ForeignKey('ConditionSet')
    isPositive = models.BooleanField(default=True)


class ConditionSet(models.Model):
    conditionSet = models.ForeignKey('Recommendation')