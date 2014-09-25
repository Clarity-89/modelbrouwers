from datetime import timedelta, date
import calendar

from dateutil.relativedelta import relativedelta

from django.db.models import Count
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin

from utils.views import LoginRequiredMixin
from .models import GroupBuild, GroupbuildStatuses as GBStatuses, Participant
from .forms import GroupBuildForm, DateForm, ParticipantForm


class GroupBuildListView(ListView):
    model = GroupBuild

    def get_queryset(self):
        return GroupBuild.public.all().annotate(n_participants=Count('participants'))

    def get_context_data(self, **kwargs):
        now = timezone.now()

        new_concepts = self.object_list.filter(status=GBStatuses.concept).order_by('?')[:5]
        starting_soon = self.object_list.filter(
            status=GBStatuses.accepted,
            start__gte=now + timedelta(days=3),
            start__lte=now + timedelta(weeks=6)
        ).order_by('start')

        dates = []
        form = DateForm(self.request.GET)
        today = form.get_date() or now.date()
        for i in range(0, 6):
            dates.append(today + relativedelta(months=i))

        offset_today = 100 / 6.0 * today.day / calendar.monthrange(today.year, today.month)[1]

        kwargs.update({
            'statuses': GBStatuses.choices,
            'new_concepts': new_concepts,
            'starting_soon': starting_soon,
            'calendar_gbs': self.get_calendar_builds(dates),
            'dates': dates,
            'offset_today': offset_today,
        })
        return super(GroupBuildListView, self).get_context_data(**kwargs)

    def get_calendar_builds(self, dates):
        start_date = date(dates[0].year, dates[0].month, 1)
        year, month = dates[-1].year, dates[-1].month
        end_date = date(year, month, calendar.monthrange(year, month)[1])

        qs = self.object_list.filter(
            status__in=GBStatuses.date_bound_statuses,
            end__gt=start_date,
            start__lt=end_date
        ).order_by('start', '-duration', '-end')
        for gb in qs:
            gb.set_calendar_dimensions(start_date, end_date, num_months=len(dates))
        return qs


class GroupBuildCreateView(LoginRequiredMixin, CreateView):
    """ TODO: webtest """
    model = GroupBuild
    template_name = 'groupbuilds/create.html'
    form_class = GroupBuildForm

    def get_form_kwargs(self):
        kwargs = super(GroupBuildCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_initial(self):
        initial = super(GroupBuildCreateView, self).get_initial()
        initial['admins'] = self.request.user
        return initial


class GroupBuildDetailMixin(object):
    """ Mixin that checks the queryset for detail-related views """
    queryset = GroupBuild.public.all()

    def get_queryset(self): # TODO: unit test
        user = self.request.user
        if user.is_authenticated(): # TODO: add staff permissions
            return (user.admin_groupbuilds.all() | self.queryset).distinct()
        return super(GroupBuildDetailMixin, self).get_queryset()


class GroupBuildDetailView(GroupBuildDetailMixin, DetailView):
    model = GroupBuild
    context_object_name = 'gb'

    def get_context_data(self, **kwargs):
        ctx = super(GroupBuildDetailView, self).get_context_data(**kwargs)
        ctx['participants'] = self.object.participant_set.all().order_by('id')
        ctx['participate_form'] = ParticipantForm()
        return ctx


class GroupBuildUpdateView(LoginRequiredMixin, UpdateView):
    model = GroupBuild
    template_name = 'groupbuilds/edit.html'
    form_class = GroupBuildForm

    def get_form_kwargs(self):
        kwargs = super(GroupBuildUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_queryset(self):
        if self.request.user.is_superuser:
            return GroupBuild.objects.all()
        return self.request.user.admin_groupbuilds.all()



class GroupBuildParticipateView(LoginRequiredMixin, GroupBuildDetailMixin,
                                CreateView, SingleObjectTemplateResponseMixin,
                                SingleObjectMixin):
    model = Participant
    form_class = ParticipantForm
    context_object_name = 'gb'
    template_name = 'groupbuilds/groupbuild_detail.html'

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def form_valid(self, form):
        form.instance.groupbuild = self.get_object()
        form.instance.user = self.request.user
        response = super(GroupBuildParticipateView, self).form_valid(form)
        messages.success(self.request, _('You\'re now listed as participant!'))
        return response

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(GroupBuildParticipateView, self).get_context_data(**kwargs)
        context['participate_form'] = context['form']
        return context
