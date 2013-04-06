from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
import datetime
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from django.contrib.auth.models import User


class Answer(models.Model):
    ans_text= models.TextField()
    
    def __unicode__(self):
        return self.ans_text

    
class Question(models.Model):
    
    ques_text = models.TextField("question")
    answers = models.ManyToManyField(Answer, related_name="choices", help_text="available choices")
#    correct_answer= models.ForeignKey(Answer, null=False, blank=False)
    
    def __unicode__(self):
        return self.ques_text

class SurveyManager(models.Manager):

    def surveys_for(self, recipient):
        recipient_type = ContentType.objects.get_for_model(recipient)
        return Survey.objects.filter(visible=True,recipient_type=recipient_type, recipient_id=recipient.id)

    
class Survey(models.Model):
    """
    A ``Survey`` is the activity of gathering answers based on a
    ``Questionnaire``. This allows you to run one or more surveys using the
    same Questionnaire, but obviously capturing difference answers.
    """
    title   = models.CharField(_('survey title'), max_length=80)
    slug    = models.SlugField(_('slug'), unique=True)
    description= models.TextField(verbose_name=_("description"),
                            help_text=_("This field appears on the public web site and should give an overview to the interviewee"),
                            blank=True)
    questions = models.ManyToManyField(Question)
    ## Add validation on datetimes
    opens   = models.DateTimeField(_('survey starts accepting submissions on'))
    closes  = models.DateTimeField(_('survey stops accepting submissions on'))
    # Define the behavior of the survey
    is_acitve = models.BooleanField(_('survey is visible'))
    public  = models.BooleanField(_('survey results are public'))
    restricted = models.BooleanField(verbose_name=_("restrict the survey to authentified user")
                                     ,blank=True,default=False)

    created_by = models.ForeignKey(User, related_name="created_surveys")
    
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    objects = SurveyManager()
    
    
    class Admin:
        list_display = ("id",)
        

    @property
    def _cache_name(self):
        if not self.id:
            id = 'new'
        else:
            id = int(self.id)
        return 'survey_' + repr(id) + '_status'

    @property
    def open(self):
        if not self.visible: return False
        value = cache.get(self._cache_name)
        if value is not None: return value
        now = datetime.datetime.now()
        if self.opens >= now:
            value = False
            duration = (now - self.opens).seconds
        elif self.closes >= now:
            value = True
            duration = (self.opens - now).seconds
        else:
            value = False
            duration = 60*60*24*31
        if duration:
            cache.set(self._cache_name, value, duration)
        return value

    @property
    def closed(self):
        return not self.open

    @property
    def status(self):
        if not self.visible: return _('private')
        if self.open: return _('open')
        if datetime.now() < self.opens:
            return unicode(_('opens ')) + datefilter(self.opens)
        return _('closed')

    @property
    def answer_count(self):
        if hasattr(self, '_answer_count'):
            return self._answer_count
        self._answer_count = sum(q.answer_count for q in self.questions.iterator())
        return self._answer_count

    @property
    def interview_count(self):
        # NOTSURE: Do we realy need this optimisation?
        if hasattr(self, '_interview_count'):
            return self._interview_count
        self._interview_count = len(Answer.objects.filter(
            survey=self.id).values('interview_uuid').distinct())
        return self._interview_count

    @property
    def session_key_count(self):
        # NOTSURE: Do we realy need this optimisation?
        if hasattr(self, '_session_key_count'):
            return self._submission_count
        self._submission_count = len(Answer.objects.filter(
            survey=self.id).values('session_key').distinct())
        return self._submission_count


    def has_answers_from(self, session_key):
        return bool(
            Answer.objects.filter(session_key__exact=session_key.lower(),
            survey__exact=self.id).distinct().count())



    def __unicode__(self):
        return u' - '.join([self.slug, self.title])

    class Admin:
        list_display = ('__unicode__', 'visible', 'public',
                        'opens', 'closes', 'open')

    @models.permalink
    def get_absolute_url(self):
        return ('survey-detail', (), {'survey_slug': self.slug })

    def save(self):
        res = super(Survey, self).save()
        cache.delete(self._cache_name)
        return res

    def answers_viewable_by(self, user):
        if not self.visible: return False
        if self.public: return True
        if user.is_anonymous(): return False
        return user.has_perm('survey.view_answers')

