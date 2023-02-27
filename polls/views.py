from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.urls import reverse
from django.views.generic import (
                                    ListView, DetailView,
                                  )
from django.db import models


class IndexView(ListView):
    template_name: str = "polls/index.html"
    context_object_name: str = "list_latest_questions"

    def get_queryset(self) -> Question:
        return Question.objects.order_by('-pub_date')[:]


class DetailsView(DetailView):
    model: models.Model = Question
    template_name: str = "polls/detail.html"


class ResultsView(DetailView):
    model: models.Model = Question
    template_name: str = "polls/results.html"


def vote(request: HttpRequest, question_id: str) -> HttpResponseRedirect or render:
    question: get_object_or_404 = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice: Choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # reloads the voting form in the question detail page
        message: str = "You've not selected any choice"
        return render(
            request, 'polls/detail.html',
            {'question': question, 'error_message': message}
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
