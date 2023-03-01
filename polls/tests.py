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

    def test_no_question(self) -> None:
        """Return an appropriate message if there are no questions
        """
        response: TestCase = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There\'re no questions available")
        self.assertQuerysetEqual(response.context['list_latest_questions'], [],)

    def test_past_question(self) -> None:
        """Display questions whose publication dates are set in the past with any number of days
        """
        question: Question = create_question(question_text="This is a past question", days=-40)
        response: TestCase = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['list_latest_questions'], [question])

    def test_two_past_question(self) -> None:
        """Display multiple past questions with publication dates set in the future
        """
        question: Question = create_question(question_text="Also a past question", days=-10)
        question_1: Question = create_question(question_text="This is another past question", days=-6)
        response: TestCase = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['list_latest_questions'], [question_1, question])

    def test_future_question(self) -> None:
        """Don't display any question whose date is set in the future with any number of days
        """
        create_question(question_text="This is a test future question", days=10)
        response: TestCase = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['list_latest_questions'], [],)

    def test_future_and_past_question(self) -> None:
        """Does not display a future question but, displays a past question instead
        """
        create_question(question_text="OH no, yet another future question", days=30)
        question: Question = create_question(question_text="This is yet again another past question", days=-60)
        response: TestCase = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['list_latest_questions'], [question],)
