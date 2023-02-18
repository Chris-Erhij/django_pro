from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader
from typing import List, Dict
from .models import Question


def index(request: HttpRequest) -> HttpResponse:
    list_latest_questions: List = Question.objects.order_by('-pub_date')[:]
    template: loader = loader.get_template('polls/index.html')
    context: Dict = {
        'list_latest_questions': list_latest_questions
    }
    return HttpResponse(template.render(context, request))


def detail(request: HttpRequest, question_id: int) -> render:
    question: Question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request: HttpRequest, question_id: int) -> HttpResponse:
    question: get_object_or_404 | Question = get_object_or_404(Question, pk=question_id)
    return HttpResponse(request, 'polls/result.html', {'question': question})


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    