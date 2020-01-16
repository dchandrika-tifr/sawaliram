"""Define the data models for all Sawaliram content"""

import datetime
from django.db import models
from django.conf import settings

from django.utils.text import slugify
from django.utils.translation import get_language_info

from dashboard.mixins.draftables import (
    DraftableModel,
    PublishedDraftableManager,
    SubmittedDraftableManager,
    DraftDraftableManager,
)
from dashboard.mixins.translations import (
    TranslationMixin,
    translatable,
)

LANGUAGE_CODES = {
    'english': 'en',
    'hindi': 'hi',
    'bengali': 'bn',
    'malayalam': 'ml',
    'marathi': 'mr',
    'tamil': 'ta',
    'telugu': 'te'
}

class Dataset(models.Model):
    """Define the data model for submitted datasets"""

    question_count = models.CharField(max_length=100)
    submitted_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='submitted_datasets',
        on_delete=models.PROTECT)
    status = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class QuestionArchive(models.Model):
    """Define the data model for raw submissions by volunteers"""

    class Meta:
        db_table = 'question_archive'

    school = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='')
    student_name = models.CharField(max_length=100)
    student_gender = models.CharField(max_length=100, default='')
    student_class = models.CharField(max_length=100, default='')
    question_text = models.CharField(max_length=1000)
    question_text_english = models.CharField(max_length=1000, default='')
    question_format = models.CharField(max_length=100)
    question_language = models.CharField(max_length=100)
    contributor = models.CharField(max_length=100)
    contributor_role = models.CharField(max_length=100)
    context = models.CharField(max_length=100)
    medium_language = models.CharField(max_length=100)
    curriculum_followed = models.CharField(max_length=100, default='')
    published = models.BooleanField(default=False)
    published_source = models.CharField(max_length=200, default='')
    published_date = models.DateField(default=datetime.date.today)
    question_asked_on = models.DateField(null=True)
    notes = models.CharField(max_length=1000, default='')
    submitted_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='archived_questions',
        on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def accept_question(self, acceptor):
        """
        Mark a question as approved, by the given acceptor (user).

        This basically changes a question from unmoderated to moderated
        by removing the QuestionArchive record and replacing it with
        a Question one.
        """

        q = Question()
        q.school = self.school
        q.area = self.area
        q.state = self.state
        q.student_name = self.student_name
        q.student_gender = self.student_gender
        q.student_class = self.student_class
        q.question_text = self.question_text
        q.question_text_english = self.question_text_english
        q.question_format = self.question_format
        q.question_language = self.question_language
        q.contributor = self.contributor
        q.contributor_role = self.contributor_role
        q.context = self.context
        q.medium_language = self.medium_language
        q.curriculum_followed = self.curriculum_followed
        q.published = self.published
        q.published_source = self.published_source
        q.published_date = self.published_date
        q.question_asked_on = self.question_asked_on
        q.notes = self.notes
        q.created_on = self.created_on
        q.updated_on = self.updated_on
        q.submitted_by = self.submitted_by
        q.curated_by = acceptor
        try:
            q.save()
            self.delete()
        except Exception as e:
            print('Error accepting question: %s' % e)

    def __str__(self):
        return self.question_text


class Question(models.Model):
    """Define the data model for questions curated by admins."""

    class Meta:
        db_table = 'question'

    school = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='')
    student_name = models.CharField(max_length=100)
    student_gender = models.CharField(max_length=100, default='')
    student_class = models.CharField(max_length=100, default='')
    question_text = models.CharField(max_length=1000)
    question_text_english = models.CharField(max_length=1000, default='')
    question_format = models.CharField(max_length=100)
    question_language = models.CharField(max_length=100)
    contributor = models.CharField(max_length=100)
    contributor_role = models.CharField(max_length=100)
    context = models.CharField(max_length=100)
    medium_language = models.CharField(max_length=100)
    curriculum_followed = models.CharField(max_length=100, default='')
    published = models.BooleanField(default=False)
    published_source = models.CharField(max_length=200, default='')
    published_date = models.DateField(default=datetime.date.today)
    question_asked_on = models.DateField(null=True)
    notes = models.CharField(max_length=1000, default='')
    dataset_id = models.CharField(max_length=100, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    curated_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='curated_questions',
        on_delete=models.PROTECT,
        default='')
    encoded_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='encoded_questions',
        on_delete=models.PROTECT,
        default='',
        blank=True,
        null=True)
    # data members for encoding
    field_of_interest = models.CharField(max_length=100, default='')
    subject_of_session = models.CharField(max_length=100, default='')
    question_topic_relation = models.CharField(max_length=100, default='')
    motivation = models.CharField(max_length=100, default='')
    type_of_information = models.CharField(max_length=100, default='')
    source = models.CharField(max_length=100, default='')
    curiosity_index = models.CharField(max_length=100, default='')
    urban_or_rural = models.CharField(max_length=100, default='')
    type_of_school = models.CharField(max_length=100, default='')
    comments_on_coding_rationale = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    """Define the data model for answers in English"""

    class Meta:
        db_table = 'answer'

    answer_text = models.TextField()
    language = models.CharField(
        max_length=100,
        default='en')
    question_id = models.ForeignKey(
        'Question',
        related_name='answers',
        on_delete=models.PROTECT,
        default='')
    status = models.CharField(max_length=50, default='submitted')
    submitted_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='answers',
        on_delete=models.PROTECT,
        default='')
    approved_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='approved_answers',
        on_delete=models.PROTECT,
        default='',
        null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return unicode representation of this Answer'''

        return 'Answer [{}]: {}'.format(
            self.question_id.question_language,
            self.question_id.question_text,
        )

    def get_language_name(self):
        """
        Return the full language name
        """
        for language, code in LANGUAGE_CODES.items():
            if code == self.language:
                return language


class AnswerComment(models.Model):
    """Define the data model for comments on Answers"""

    class Meta:
        db_table = 'answer_comment'

    text = models.TextField()
    answer = models.ForeignKey(
        'Answer',
        related_name='comments',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='answer_comments',
        on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class AnswerCredit(models.Model):
    """Define the data model for answer and article credits"""

    class Meta:
        db_table = 'answer_credit'
        ordering = ['id']

    credit_title = models.CharField(max_length=50)
    credit_user_name = models.CharField(max_length=50)
    is_user = models.BooleanField(default=False)
    user = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='answer_credits',
        on_delete=models.PROTECT,
        default='',
        null=True)
    answer = models.ForeignKey(
        'Answer',
        related_name='credits',
        on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class UncuratedSubmission(models.Model):
    """Define the data model to store submissions pending for curation"""

    class Meta:
        db_table = 'uncurated_submission'

    submission_method = models.CharField(max_length=50)
    submission_id = models.IntegerField()
    number_of_questions = models.IntegerField()
    excel_sheet_name = models.CharField(max_length=100)
    submitted_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='submissions',
        on_delete=models.PROTECT,
        default='')
    curated = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class UnencodedSubmission(models.Model):
    """Define the data model to store submissions pending for encoding"""

    class Meta:
        db_table = 'unencoded_submission'

    submission_id = models.IntegerField(null=True)
    number_of_questions = models.IntegerField()
    excel_sheet_name = models.CharField(max_length=100)
    encoded = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class TranslatedQuestion(models.Model):
    """Define the data model to store translated questions"""

    class Meta:
        db_table = 'translated_question'

    question_id = models.ForeignKey(
        'Question',
        related_name='translations',
        on_delete=models.PROTECT,
        default='')
    question_text = models.CharField(max_length=1000)
    language = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

@translatable
class Article(DraftableModel):
    '''
    Complete data model holding all kinds of articles. This includes:
      * ArticleDraft
      * SubmittedArticle
      * Article

    This is internally tracked via the 'status' parameter. You can
    also query articles with the specified status by using its proxy
    model (which internally checks the 'status' prameter before
    returning results).
    '''

    translation_model = 'dashboard.PublishedArticleTranslation'
    translatable_fields = ['title', 'body']

    title = models.CharField(max_length=1000, null=True)
    language = models.CharField(max_length=100,
        choices=settings.LANGUAGE_CHOICES,
        default='en')
    author = models.ForeignKey('sawaliram_auth.User',
        related_name='articles',
        on_delete=models.PROTECT,
        default='',
        null=True)

    body = models.TextField(null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    approved_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='approved_articles',
        on_delete=models.PROTECT,
        default='',
        null=True)
    published_on = models.DateTimeField(auto_now_add=True)

    def get_slug(self):
        return slugify(self.title)

    class Meta:
        db_table = 'articles'

class ArticleDraft(Article.get_draft_model(), Article):
    objects = DraftDraftableManager()
    class Meta:
        proxy = True

class SubmittedArticle(Article.get_submitted_model(), Article):
    objects = SubmittedDraftableManager()
    class Meta:
        proxy = True

class PublishedArticle(Article.get_published_model(), Article):
    objects = PublishedDraftableManager()
    class Meta:
        proxy = True

class ArticleComment(models.Model):
    """Define the data model for comments on Answers"""

    class Meta:
        db_table = 'article_comment'

    text = models.TextField()

    article = models.ForeignKey(
        'Article',
        related_name='comments',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='article_comments',
        on_delete=models.PROTECT)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class ArticleTranslation(DraftableModel, TranslationMixin):
    '''
    Stores translated data for a given article
    '''

    # What we're translating
    source = models.ForeignKey(
        'Article',
        related_name='translations',
        on_delete=models.CASCADE)

    # Translated Fields

    title = models.CharField(max_length=1000, null=True)
    body = models.TextField(null=True)

class PublishedArticleTranslation(
    ArticleTranslation.get_published_model(),
    ArticleTranslation
):
    objects = PublishedDraftableManager()
    class Meta:
        proxy = True
