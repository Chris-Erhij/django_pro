from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.urls import reverse
from django.views.generic import (
                                    ListView, DetailView,
                                  )
from django.utils import timezone
from typing import Type


class IndexView(ListView):
    template_name: str = "polls/index.html"
    context_object_name: str = "list_latest_questions"  # Overrides 'question', django's default context object name.

    def get_queryset(self):
        """Return a list of all published questions past and recent

        Excluding the ones published with dates set into the
        future with any x numbers of days"""

        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:]


class DetailsView(DetailView):
    model = Question
    template_name: str = "polls/detail.html"

    def get_queryset(self):
        """Only return question which are published in past and recently

           i.e. Question whose publication dates is less than or equal to current time
           using dunder lte (__lte)
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(DetailView):
    model = Question
    template_name: str = "polls/results.html"


def vote(request: HttpRequest, question_id: str) -> HttpResponseRedirect | HttpResponse:
    question: Question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice: Choice  = question.choice_set.get(pk=request.POST['choice']) # type: ignore
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

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) # type: ignore
