import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from django.urls import reverse

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self) -> None:
        time_now: datetime = timezone.now() + datetime.timedelta(days=30)
        future_question: Question = Question(pub_date=time_now)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self) -> None:
        time_now: datetime = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question: Question = Question(pub_date=time_now)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_past_question(self) -> None:
        time_now: datetime = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question: Question = Question(pub_date=time_now)
        self.assertIs(past_question.was_published_recently(), False)


def create_question(question_text: str, days: int) -> Question:
    """Create and return a Question object

    question_text for question and date published with the given number of days offset to now
    (negative for questions published in the past, positive for question published in the future
    """
    time: timezone = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):

    def test_no_question(self) ->:
        """Return an appropriate message if there are no questions
        """
