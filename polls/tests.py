import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse
# Create your tests here.

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """当问题发布时间是未来时，was_published_recently()返回false"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    def test_was_published_recently_with_old_question(self):
        """"""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    def test_was_published_recently_with_recent_question(self):
        """当差一秒一天时返回True"""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_quetion = Question(pub_date=time)
        self.assertIs(recent_quetion.was_published_recently, True)
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """如果没有问题存在，则有正确的提示信息"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """正确展示过去的问题"""
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """不展示未来的问题"""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """正确展示过去和未来的问题"""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
    def test_two_past_questions(self):
        """正确展示多个过去的问题"""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>'])

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
