from django.test import TestCase
from django.urls import resolve
from django.urls import reverse
from django.http import HttpRequest
from .views import WorkoutEntryView, dashboard, social
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory, Client
from .models import Dashboard, QuestCompleted
from friendship.models import Follow

from requests.auth import HTTPBasicAuth


from . import views
from .views import leaderboard
from .views import SearchListView
from .views import follow
# Create your tests here.

class DummyTestCase(TestCase):
    def setUp(self):
        x = 1

    def test_dummy_test_case(self):
        self.assertEqual(1, 1)


class ClientTest(TestCase):
    csrf_client = Client(enforce_csrf_checks=True)


class WorkoutEntryViewTestCase(TestCase):
    longMessage = True

    def test_get(self):
        status_code = 200
        view_class = views.WorkoutEntryView

        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.WorkoutEntryView.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)

class SearchListViewTestCase(TestCase):
    '''longMessage = True
    view_class = views.SearchListViewView

    def test_get(self):
        status_code = 200
        view_class = views.SearchListView

        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.SearchListView.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)'''

    '''def test_root_url_resolves_to_search_view(self):
        found = resolve('/')
        self.assertEqual(found.func, SearchListView)'''

    def search_view(self):
        resolver = resolve('/search/')
        self.assertEqual(resolver.view_name, 'search')

class Urlspatterns(TestCase):
    def test_dashboard_redirect(self):
        url = reverse('exercise:dashboard')
        self.assertEqual(url, '/dashboard/')

    def test_newworkout_redirect(self):
        url = reverse('exercise:new_workout')
        self.assertEqual(url, '/new-workout/')

    def test_social_redirect(self):
        url = reverse('exercise:social')
        self.assertEqual(url, '/social/')

    def test_leaderboard_redirect(self):
        url = reverse('exercise:leaderboard')
        self.assertEqual(url, '/leaderboard/')

    def test_gym_redirect(self):
        url = reverse('exercise:nearby-gyms')
        self.assertEqual(url, '/nearby-gyms/')
