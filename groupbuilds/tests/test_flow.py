""" Test all the flow components"""
from django.test import TestCase
from django.core.urlresolvers import reverse

from users.tests.factory_models import UserFactory

from .factories import GroupBuildFactory
from ..models import GroupbuildStatuses, GroupBuild

# TODO: use webtest

class FlowTest(TestCase):
#     def test_user_concept(self):
#         """ Test that a regular user can create a concept """

    def test_user_can_see_administrated_detail(self):
        """ GB admins must be able to (pre)view the detail page of a GB """
        # create groupbuild with not publicly visible status
        groupbuild = GroupBuildFactory(status=GroupbuildStatuses.denied)
        self.assertNotIn(groupbuild, GroupBuild.public.all())

        user = UserFactory(username='testuser', password='password')
        groupbuild.admins.add(user)

        # response = self.client.get(groupbuild.get_absolute_url())
        # self.assertEqual(response.status_code, 404)

        # log in
        self.client.login(username='testuser', password='password')
        response = self.client.get(groupbuild.get_absolute_url())
        self.assertEqual(response.status_code, 200)

#     def test_user_participant(self):
#         pass

#     def test_user_edit(self):
#         pass

    def test_user_submit(self):
        """ Test that the user can submit the concept """
        user1 = UserFactory.create()
        user2 = UserFactory.create()

        groupbuild = GroupBuildFactory.create(status=GroupbuildStatuses.concept)
        groupbuild.admins.add(user1, groupbuild.applicant)
        self.assertEqual(groupbuild.admins.count(), 2)

        # test that user2 cannot submit the groupbuilds
        self.client.login(username=user2.username, password='password')
        url = reverse('groupbuilds:submit', kwargs={'slug': groupbuild.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        self.client.logout

        self.client.login(username=user1, password='password')
        url = reverse('groupbuilds:submit', kwargs={'slug': groupbuild.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        response = self.client.post(url)
        self.assertEquals(response.status_code, 302)
        groupbuild = GroupBuild.objects.get(slug=groupbuild.slug)
        self.assertEquals(groupbuild.status, GroupbuildStatuses.submitted)


#     def test_submitted_concept_not_editable(self):
#         pass

#     def test_pm_sent_after_submit(self):
#         """ Test that a pm is sent to the mods/post is made in mod forum """

#     def test_mod_can_edit(self):
#         """ Test that a moderator can edit a group build """

#     def test_approval(self):
#         """ Test that mods can approve group builds and that confirmation is sent """

#     def test_dates_locked_for_non_staff(self):
#         """
#         Test that the dates are not editable when the groupbuild is out of the
#         concept state
#         """

#     def test_user_can_edit_approved_and_denied(self):
#         """ Users can edit in all states, and resubmit """

#     def test_participant_stats(self):
#         """ Test that the statistics are updated when a participant signs up """
