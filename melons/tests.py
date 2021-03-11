from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import *
import six


'''The following tests related to registration is referenced from 
https://github.com/CryceTruly/djangoauthenticationapp '''


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


generate_token = TokenGenerator()


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'password',
            'password2': 'password',
            'name': 'fullname'
        }
        self.user_short_password = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'tes',
            'password2': 'tes',
            'name': 'fullname'
        }
        self.user_unmatching_password = {

            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'teslatt',
            'password2': 'teslatto',
            'name': 'fullname'
        }

        self.user_invalid_email = {

            'email': 'test.com',
            'username': 'username',
            'password': 'teslatt',
            'password2': 'teslatto',
            'name': 'fullname'
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_cant_register_user_withshortpassword(self):
        response = self.client.post(self.register_url, self.user_short_password, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_cant_register_user_with_unmatching_passwords(self):
        response = self.client.post(self.register_url, self.user_unmatching_password, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_cant_register_user_with_invalid_email(self):
        response = self.client.post(self.register_url, self.user_invalid_email, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_cant_register_user_with_taken_email(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 400)


class LoginTest(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_login_success(self):
        self.client.post(self.register_url, self.user, format='text/html')
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_cantlogin_with_unverified_email(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 401)

    def test_cantlogin_with_no_username(self):
        response = self.client.post(self.login_url, {'password': 'passwped', 'username': ''}, format='text/html')
        self.assertEqual(response.status_code, 401)

    def test_cantlogin_with_no_password(self):
        response = self.client.post(self.login_url, {'username': 'passwped', 'password': ''}, format='text/html')
        self.assertEqual(response.status_code, 401)


class UserVerifyTest(BaseTest):
    def test_user_ctivates_success(self):
        user = User.objects.create_user('testuser', 'crytest@gmail.com')
        user.set_password('tetetebvghhhhj')
        user.is_active = False
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = generate_token.make_token(user)
        response = self.client.get(reverse('activate', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='crytest@gmail.com')
        self.assertTrue(user.is_active)

    def test_user_cant_ctivates_succesfully(self):
        user = User.objects.create_user('testuser', 'crytest@gmail.com')
        user.set_password('tetetebvghhhhj')
        user.is_active = False
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = generate_token.make_token(user)
        response = self.client.get(reverse('activate', kwargs={'uidb64': 'uid', 'token': 'token'}))
        self.assertEqual(response.status_code, 401)
        user = User.objects.get(email='crytest@gmail.com')
        self.assertFalse(user.is_active)


class ProfileViewTest(TestCase):
    def setup(self):
        self.empty_form = {
            'last_name': '',
            'first_name': '',
            'titles': '',
            'DOB': '',
            'team': '',
            'society': '',
            'nickname': '',
            'email': '',
            'course': ''
        }
        self.success_form = {
            'last_name': 'Test',
            'first_name': 'Guy',
            'titles': 'Student',
            'DOB': '2000-01-01',
            'team': 'T1',
            'society': 'T1',
            'nickname': 'TG',
            'email': 'email@email.com',
            'course': 'T1'
        }

    def AvatarChangeTest(self):
        c = Client()
        c.login()
        user = User.objects.create_user('testuser', 'crytest@gmail.com')
        user.set_password('tetetebvghhhhj')
        user.is_active = False
        # posting an invalid file as avatar
        with open('static/testing/testing.docx') as t1:
            response = c.post('/profile/', {'name': 'testing.docx', 'attachment': t1})
            self.assertEqual(response, 200)

        # posting a valid file as avatar
        with open('static/testing/testing.JPG') as t2:
            response = c.post('/profile/', {'name': 'testing.docx', 'attachment': t2})
            self.assertEqual(response, 200)

        t1.close()
        t2.close()

    def EmptyFormTest(self):
        c = Client()
        c.login()
        response = c.post('/profile/', self.empty_form)
        self.assertEqual(response, 200)

    def SuccessFormTest(self):
        c = Client()
        c.login()
        response = c.post('/profile/', self.success_form)
        self.assertEqual(response, 200)


class ShopViewTest(TestCase):
    def setup(self):
        self.invalid_form = {
            'invalid_key': 'inv'
        }
        self.valid_form = {
            'resource': 100,
            'new_item': 'Melon',
        }

    def BaseTest(self):
        c = Client()
        c.login()
        response = c.get('/shop/')
        self.assertEqual(response, 200)

    def ValidFormTest(self):
        c = Client()
        c.login()
        response = c.post('/shop/', self.invalid_form)
        self.assertEqual(response, 200)

    def InvalidFormTest(self):
        c = Client()
        c.login()
        response = c.post('/shop/', self.valid_form)
        self.assertEqual(response, 200)


class AnswerQuizTest(TestCase):
    def setup(self):
        self.valid_target = Collection.objects.create(coll_title='Test', coll_description='Test', coll_creator=User.objects.create_user('tu','tu@tu.com','abc'))
        self.valid_target.save()
        self.invalid_form = {
            'i': ''
        }
        self.valid_form = {
            'i': self.valid_target.coll_id
        }

    def InvalidFormTest(self):
        c = Client()
        c.login()
        response = c.post('/answer_quiz/', self.invalid_form)
        self.assertEqual(response, 200)

    def ValidFormTest(self):
        c = Client()
        c.login()
        response = c.post('/answer_quiz/', self.valid_form)
        self.assertEqual(response, 200)


class ResultViewTest(TestCase):
    def setup(self):
        self.invalid_form = {
            'random_index': ''
        }
        self.valid_form = {
            'question_num': '5',
        }

    def InvalidFormTest(self):
        c = Client()
        c.login()
        response = c.post('/result/', self.invalid_form)
        self.assertEqual(response, 200)

    def ValidFormTest(self):
        c = Client()
        c.login()
        response = c.post('/result/', self.valid_form)
        self.assertEqual(response, 200)


class FlashCardViewTest(TestCase):
    def setup(self):
        self.invalid_form = {
            'random_index': ''
        }
        self.valid_form = {
            'current_card': 'a',
        }

    def InvalidFormTest(self):
        c = Client()
        c.login()
        response = c.post('/result/', self.invalid_form)
        self.assertEqual(response, 200)

    def ValidFormTest(self):
        c = Client()
        c.login()
        response = c.post('/result/', self.valid_form)
        self.assertEqual(response, 200)

    def GetTest(self):
        c = Client()
        c.login()
        response = c.get('/result/')
        self.assertEqual(response, 200)


class CardSetListViewTest(TestCase):
    def BaseTest(self):
        c = Client()
        c.login()
        response = c.get('/card_set_list/')
        self.assertEqual(response, 200)