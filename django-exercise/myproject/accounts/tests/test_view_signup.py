from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import signup
from ..forms import SignUpForm


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SignUpSuccessfulTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'foobar',
            'email': 'foobar@foo.bar',
            'password1': 'a_secret_pass_123',
            'password2': 'a_secret_pass_123',
        }
        self.response = self.client.post(url, data)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_auth(self):
        home_url = reverse('home')
        a_get_response = self.client.get(home_url)
        user = a_get_response.context.get('user')
        self.assertTrue(user.is_authenticated)


class SignUpInvalidTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_signup_error(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_no_user_creation(self):
        self.assertFalse(User.objects.exists())

