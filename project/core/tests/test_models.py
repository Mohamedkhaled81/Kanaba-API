"""
Test Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user_data(**kwargs):
    user_data = {
        'email': 'test@example.com',
        'first_name': 'test',
        'last_name': 'test2',
        'password': '12345pass',
        'role': 'Customer',
        }
    user_data.update(kwargs)

    return user_data


class TestModels(TestCase):

    def test_create_customer(self):
        user_data = create_user_data(role='Customer')
        user = get_user_model().objects.create_user(**user_data)

        self.assertIn(user, get_user_model().objects.all())
        self.assertEqual(
            user,
            get_user_model().objects.get(user_id=user.user_id))

        self.assertTrue(user.check_password(user_data['password']))
        self.assertTrue(user.role, user_data['role'])

    def test_creat_user_without_email(self):
        user_data = create_user_data(email='')

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                **user_data
            )

    def test_creat_user_wihtout_password(self):
        user_data = create_user_data(password='')

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                **user_data
            )

    def test_create_superuser(self):
        user_data = create_user_data(role='Admin')

        user = get_user_model().objects.create_superuser(**user_data)
        self.assertIn(user, get_user_model().objects.all())
        self.assertEqual(
            user,
            get_user_model().objects.get(user_id=user.user_id))

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.role, user_data['role'])

    def test_create_designer(self):
        user_data = create_user_data(role='Desginer')

        user = get_user_model().objects.create_user(**user_data)
        self.assertIn(user, get_user_model().objects.all())
        self.assertEqual(
            user,
            get_user_model().objects.get(user_id=user.user_id))

        self.assertEqual(user.role, user_data['role'])

    def test_create_tenant(self):
        user_data = create_user_data(role='Tenant')

        user = get_user_model().objects.create_user(**user_data)
        self.assertIn(user, get_user_model().objects.all())
        self.assertEqual(
            user,
            get_user_model().objects.get(user_id=user.user_id))

        self.assertEqual(user.role, user_data['role'])
