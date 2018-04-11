from django.test import TestCase
from hc.front.models import Question, Answer
 
class FaqsTestCase(TestCase):

    def test_can_create_question(self):
        q = Question(question_text ="what does healthchecks do?")
        q.save()
        total_quiz = Question.objects.count()
        self.assertEqual(total_quiz, 1)
        self.assertEqual(str(q), "what does healthchecks do?")

    def test_can_answer_question(self):
        q = Question(question_text ="what does healthchecks do?")
        q.save()
        q.answer_set.create(answer_text = "it monitors your cron jobs" )
        total_answers = q.answer_set.count()
        self.assertEqual(total_answers, 1)
        self.assertEqual(str(q.answer_set.all()[0]),"it monitors your cron jobs" )
 
    def test_question_can_have_multiple_answers(self):
        q = Question(question_text ="what does healthchecks do?")
        q.save()
        q.answer_set.create(answer_text = "it monitors your cron jobs" )
        q.answer_set.create(answer_text = "It sends you alerts" )
        total_answers = q.answer_set.count()
        self.assertEqual(total_answers, 2)
 
    def test_answer_is_related_to_question(self):
        q = Question(question_text ="what does healthchecks do?")
        q.save()
        ans = q.answer_set.create(answer_text = "it monitors your cron jobs" )
        self.assertEqual(ans.question.question_text, "what does healthchecks do?")

    def test_user_can_view_faqs(self):
        #create a question and answer to be used by the view
        pass
