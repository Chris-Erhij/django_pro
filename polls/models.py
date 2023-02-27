from django.db import models
from django.db.models import (
    CharField, DateTimeField, ForeignKey,
    IntegerField, Model,
                              )
import datetime
from django.utils import timezone


class Question(Model):
    question_text: CharField = models.CharField(max_length=200)
    pub_date: DateTimeField | float = models.DateTimeField('date published')

    # Return question text as a string
    def __str__(self) -> CharField | str:
        return self.question_text

    def was_published_recently(self) -> bool:
        now: timezone = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(Model):
    question: ForeignKey = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text: CharField = models.CharField(max_length=200)
    votes: IntegerField = models.IntegerField(default=0)

    # Return a choice as a sting
    def __str__(self) -> CharField | str:
        return self.choice_text
