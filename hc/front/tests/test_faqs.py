from django.test import TestCase
from hc.front.models import Question, Answer
 
class FaqsTestCase(TestCase):

    def test_can_create_question(self):
        q = Question(question_text ="what does healthchecks do?")
        q.save()
        total_quiz = Question.objects.count()
        self.assertEqual(total_quiz, 1)

    def test_can_answer_question(self):
        q = Question(question_text ="what does healthchecks do?")
        q.save()
        q.answer_set.create(answer_text = "it monitors your cron jobs" )
        total_answers = q.answer_set.count()
        self.assertEqual(total_answers, 1)
 
    def test_answer_is_related_to_question(self):
        q = Question(question_text ="what does healthchecks do?")
        q.save()
        ans = q.answer_set.create(answer_text = "it monitors your cron jobs" )
        self.assertEqual(ans.question.question_text, "what does healthchecks do?")
        

