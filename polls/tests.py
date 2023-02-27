import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


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
