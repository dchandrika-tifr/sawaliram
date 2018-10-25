
from django.db import models

class Question(models.Model):

    class Meta:
        db_table = 'question'

    school = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='')
    student_name = models.CharField(max_length=100)
    student_class = models.IntegerField(default=0)
    student_age = models.IntegerField(default=0)
    question_text = models.CharField(max_length=200)
    question_text_english = models.CharField(max_length=200, default='')
    question_topic = models.CharField(max_length=100)
    question_format = models.CharField(max_length=100)
    submitted_in_question_box = models.BooleanField(default=False)
    question_language = models.CharField(max_length=100)
    contributor = models.CharField(max_length=100)
    contributor_role = models.CharField(max_length=100)
    context = models.CharField(max_length=100)
    local_language = models.CharField(max_length=100)
    medium_language = models.CharField(max_length=100)
    question_submission_date = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text