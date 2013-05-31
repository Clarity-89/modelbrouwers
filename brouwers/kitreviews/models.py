from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _


from general.utils import get_username


RATING_BASE = 100 # store ratings relative to 100
RATING_DISPLAY_BASE = 5
DEFAULT_RATING = 50
DEFAULT_DIFFICULTY = 3


class Brand(models.Model):
    """ Model for scale model brands, e.g. Revell"""
    
    name = models.CharField(_(u'brand'), max_length=100, db_index=True)
    is_active = models.BooleanField(_(u'is active?'), default=True, 
                help_text=_(u'Does the brand still exist?')
                )

    class Meta:
        verbose_name = _(u'brand')
        verbose_name_plural = _(u'brands')
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Scale(models.Model):
    """ Possible scales a model kit can be in"""
    
    scale = models.PositiveSmallIntegerField(_(u'scale'), db_index=True)

    class Meta:
        verbose_name = _(u'scale')
        verbose_name_plural = _(u'scales')
        ordering = ['scale']
    # TODO: default ordering based on amount of kits with that scale -> most popular ones one top?

    def get_repr(self, separator=":"):
        return u'1%s%d' % (separator, self.scale)

    def __unicode__(self):
        return self.get_repr()

    def unicode_slash(self):
        """ Output the scale as 1/48 instead of 1:48 """
        return self.get_repr(separator='/')

# TODO: multiple box photos?
class ModelKit(models.Model):
    """ Model containing all the data about kits, to be linked with kitreviews """
    
    brand = models.ForeignKey(Brand, verbose_name=_(u'brand'))
    kit_number = models.CharField(
                _(u'kit number'), max_length=50,
                blank=True, help_text=_(u'Kit number as found on the box.'),
                db_index=True
                )
    name = models.CharField(_(u'kit name'), max_length=255, db_index=True)
    scale = models.ForeignKey(Scale)
    duplicates = models.ManyToManyField(
                "self", blank=True, null=True, 
                verbose_name=_(u'duplicates'),
                help_text=_(u'Kits that are the same but have another producer.'),
                )

    submitter = models.ForeignKey(User)
    submitted_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = _(u'model kit')
        verbose_name_plural = _(u'model kits')

    def __unicode__(self):
        return u"%(brand)s - %(name)s" % {
            'brand': self.brand.__unicode__(),
            'name': self.name,
            }

    def clean(self):
        super(ModelKit, self).clean()
        if self.kit_number:
            # validate the uniqueness of kitnumber, scale and brand only if a kit number is supplied
            reviews = ModelKit.objects.filter(
                            brand = self.brand,
                            kit_number = self.kit_number,
                            scale = self.scale
                            )
            if reviews.exists():
                raise ValidationError(
                    _(u'A kit from %(brand)s with kit number \'%(kit_number)s\' already exists') % {
                        'brand': self.brand,
                        'kit_number': self.kit_number
                        }
                    )


class KitReview(models.Model):
    """ Model holding the review information for a model kit """

    model_kit = models.ForeignKey(ModelKit)
    raw_text = models.TextField(_(u'review text'))
    html = models.TextField(blank=True, help_text=u'raw_text with BBCode rendered as html')
    rating = models.PositiveSmallIntegerField(_(u'rating'), default=DEFAULT_RATING)
    difficulty = models.PositiveSmallIntegerField(_(u'difficulty'), default=DEFAULT_DIFFICULTY)
    # TODO: custom field voor maken met images, of jquery-ui schuifbalk?

    reviewer = models.ForeignKey(User)
    submitted_on = models.DateTimeField(auto_now_add=True)
    last_edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'kit review')
        verbose_name_plural = _(u'kit reviews')

    def __unicode__(self):
        return _(u'Review: %(kit)s by %(user)s') % {
            'kit': self.model_kit.name,
            'user': get_username(self, field='reviewer'),
        }

    @property
    def votes(self):
        votes_pos = self.kitreviewvote_set.filter(vote='+').count()
        votes_neg = self.kitreviewvote_set.filter(vote='-').count()
        votes_total = votes_pos + votes_neg
        return (votes_pos, votes_neg, votes_total)

class KitReviewVote(models.Model):
    """ Model holding the votes for kitreviews, showing the quality of the review """

    VOTE_TYPES = (
        ('+', '+'),
        ('-', '-'),
        )
    
    kit_review = models.ForeignKey(KitReview)
    vote = models.CharField(_('vote'), max_length=1, db_index=True)
    voter = models.ForeignKey(User)

    class Meta:
        verbose_name = _(u'kit review vote')
        verbose_name_plural = _(u'kit review votes')
        unique_together = (('kit_review', 'voter'),)

    def __unicode__(self):
        return _(u"Vote for review by %(review_submitter)s") % {
                    'review_submitter': get_username(self.kit_review, field=reviewer)
                    }