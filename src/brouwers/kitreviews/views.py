from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from extra_views import InlineFormSet, CreateWithInlinesView, NamedFormsetsMixin

from brouwers.utils.views import LoginRequiredMixin
from forms import *
from models import *


def index(request):
    reviews = KitReview.objects.all()
    return render(request, 'kitreviews/base.html', {'reviews': reviews})


class ReviewPropertyRatingInline(InlineFormSet):
    model = KitReviewPropertyRating

    @property
    def extra(self):
        return KitReviewProperty.objects.count()

    def get_initial(self):
        return [{'prop': prop} for prop in KitReviewProperty.objects.all()]


class AddReview(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = KitReview
    template_name = 'kitreviews/add_review.html'
    form_class = KitReviewForm
    inlines = [ReviewPropertyRatingInline]
    inlines_names = ['properties']

    def get_form_kwargs(self):
        kwargs = super(AddReview, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class FindKit(DetailView):
    pass


class KitDetail(DetailView):
    pass
