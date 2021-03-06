from datetime import date
import json

from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ungettext as _n, ugettext as _
from django.views.decorators.cache import cache_page

from brouwers.general.decorators import (login_required_403,
                                         permission_required_ajax,
                                         user_passes_test_403)
from brouwers.general.models import UserProfile
from brouwers.general.utils import (get_username_for_user, clean_username,
                                    clean_username_fallback)


from .models import ForumLinkBase, Report, ForumPostCountRestriction, ForumUser, BuildReportsForum
from .forms import ForumForm, PosterIDsForm


@cache_page(60*60*24)
def get_sync_data(request):
    response_data = {}
    t = date.today()
    links_to_be_synced = ForumLinkBase.objects.filter(enabled=True, to_date__gte=t, from_date__lte=t)
    for link in links_to_be_synced:
        response_data[link.link_id] = [l.link_id for l in link.forumlinksynced_set.all()]
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_chat(request):
    t = get_template('chat.html')
    if request.user.is_authenticated():
        nickname = get_username_for_user(request.user)
    else:
        nickname = settings.IRC_DEFAULT_NICK

    c = Context({
        'MIBBIT_SETTINGS': settings.MIBBIT_SETTINGS,
        'IRC_SERVER': settings.IRC_SERVER,
        'IRC_CHANNEL': settings.IRC_CHANNEL,
        'nickname': nickname,
    })

    html = t.render(c)
    json_data = {
        'html': html,
        'title': "Brouwers chat [%s, %s]" % (settings.IRC_SERVER, settings.IRC_CHANNEL)
    }
    return HttpResponse(json.dumps(json_data), content_type='application/json')


@permission_required_ajax('forum_tools.can_see_reports')
def get_mod_data(request):
    data = {}
    num_open_reports = Report.objects.filter(report_closed=False).count()
    data['open_reports'] = num_open_reports
    data['text_reports'] = _n("1 open report", "%(num)d open reports", num_open_reports) % {'num': num_open_reports}
    return HttpResponse(json.dumps(data), content_type="application/json")


@user_passes_test_403(lambda u: u.groups.filter(name__iexact='content sharing').exists())
def get_sharing_perms(request):
    data = {}
    form = PosterIDsForm(request.GET)
    if form.is_valid():
        forumusers = ForumUser.objects.filter(user_id__in=form.poster_ids)
        if forumusers.exists():
            # render text in template
            t_allowed = get_template('forum_tools/sharing_allowed.html')
            t_not_allowed = get_template('forum_tools/sharing_not_allowed.html')
            template_sharing_allowed = t_allowed.render(Context())
            template_sharing_not_allowed = t_not_allowed.render(Context())

            for forumuser in forumusers:
                try:
                    profile = UserProfile.objects.get(forum_nickname=forumuser.username)
                    if profile.allow_sharing:
                        data[forumuser.user_id] = template_sharing_allowed
                    else:
                        data[forumuser.user_id] = template_sharing_not_allowed
                except UserProfile.DoesNotExist:
                    data[forumuser.user_id] = template_sharing_not_allowed
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required_403
def get_posting_level(request):
    data = {}
    form = ForumForm(request.GET)
    if form.is_valid():
        forum = form.cleaned_data['forum']
        username = request.user.username
        # iexact doesn't work because MySQL tables are utf8_bin collated...
        try:
            username_cleaned = clean_username(username)
            forum_user = ForumUser.objects.get(username_clean=username_cleaned)
        except ForumUser.DoesNotExist:
            try:
                username_cleaned = clean_username_fallback(username)
                forum_user = ForumUser.objects.get(username_clean=username_cleaned)
            except ForumUser.DoesNotExist:
                # final fallback - try to read the cookie
                uid = request.COOKIES.get(settings.PHPBB_UID_COOKIE)
                forum_user = ForumUser.objects.get(pk=uid)

        # TODO: find a way to cache this... or find it out client side
        num_posts = forum_user.user_posts

        restrictions = ForumPostCountRestriction.objects.filter(forum_id=forum.forum_id)
        data['restrictions'] = [restr.posting_level for restr in restrictions if restr.min_posts > num_posts]
    return HttpResponse(json.dumps(data), content_type="application/json")


@cache_page(60*60*24*7*2)  # two weeks, cache is language based already
def get_build_report_forums(self):
    # TODO: return data if the build report was added already
    forum_ids = BuildReportsForum.objects.values_list('forum_id', flat=True)
    data = {
        'forum_ids': list(forum_ids),
        'text_build_report': _('Add build report'),
        'text_nominate': _('Nominate for award'),
    }
    return HttpResponse(json.dumps(data), content_type="application/json")
