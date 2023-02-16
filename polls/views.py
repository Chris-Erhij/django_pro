from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from typing import Any, List, Dict
from .models import Question


def index(request: Any) -> HttpResponse:
    list_latest_questions: List = Question.objects.order_by('-pub_date')[:]
    template: loader = loader.get_template('polls/index.html')
    context: Dict = {
        'list_latest_questions': list_latest_questions
    }
    return HttpResponse(template.render(context, request))


def detail(request: Any, question_id: int) -> render:
    question: Question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request: Any, question_id: int) -> HttpResponse:
    return HttpResponse("This is the vote result for question %s." % question_id)


def vote(request: Any, question_id: int) -> HttpResponse:
    response: str = "You're voting for question %s."
    return HttpResponse(response % question_id)
