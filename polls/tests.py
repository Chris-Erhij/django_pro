import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from django.urls import reverse
from django.http import HttpResponse


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self) -> None:
        time_now = timezone.now() + datetime.timedelta(days=30)
        future_question: Question = Question(pub_date=time_now)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self) -> None:
        time_now  = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question: Question = Question(pub_date=time_now)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_past_question(self) -> None:
        time_now  = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question: Question = Question(pub_date=time_now)
        self.assertIs(past_question.was_published_recently(), False)


def create_question(question_text: str, days: int) -> Question:
    """Create and return a Question object

    question_text for question and date published with the given number of days offset to now
    (negative for questions published in the past, positive for question published in the future
    """
    time  = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):

    def test_no_question(self) -> None:
        """Return an appropriate message if there are no questions
        """
        response: HttpResponse = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There\'re no questions available")
        self.assertQuerysetEqual(response.context['list_latest_questions'], [],)

    def test_past_question(self) -> None:
        """Display questions whose publication dates are set in the past with any number of days
        """
        question: Question = create_question(question_text="This is a past question", days=-40)
        response: HttpResponse = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['list_latest_questions'], [question]) # type: ignore

    def test_two_past_question(self) -> None:
        """Display multiple past questions with publication dates set in the future
        """
        question: Question = create_question(question_text="Also a past question", days=-10)
        question_1: Question = create_question(question_text="This is another past question", days=-6)
        response: HttpResponse = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['list_latest_questions'], [question_1, question]) # type: ignore

    def test_future_question(self) -> None:
        """Don't display any question whose date is set in the future with any number of days
        """
        create_question(question_text="This is a test future question", days=10)
        response: HttpResponse = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context['list_latest_questions'], [],)

    def test_future_and_past_question(self) -> None:
        """Does not display a future question but, displays a past question instead
        """
        create_question(question_text="OH no, yet another future question", days=30)
        question: Question = create_question(question_text="This is yet again another past question", days=-60)
        response: HttpResponse = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['list_latest_questions'], [question]) # type: ignore


class QuestionDetailViewTest(TestCase):
    def test_future_question(self) -> None:
        """Return a 404 not found error with questions whose publication dates are set in the future

            If a user is able to guess a url for a certain question detail, function is able to test to see if
            said question is displayed to the user.
        """
        future_question: Question = create_question(
            question_text="What are your intentions for this"
            "in the future", days=16
        )
        url: str = reverse('polls:detail', args=future_question.id) # type: ignore
        response: HttpResponse = self.client.get(url)
        self.assertContains(response.status_code, 404) # type: ignore

    def test_past_question(self) -> None:
        """Display questions whose publication dates are set in the past
        """
        past_question: Question = create_question(question_text="A past question for test purposes", days=-16)
        url: str = reverse("polls:detail", args=past_question.id,) # type: ignore
        response: HttpResponse = self.client.get(url)
        self.assertQuerysetEqual(response, past_question.question_text)  # type: ignore
