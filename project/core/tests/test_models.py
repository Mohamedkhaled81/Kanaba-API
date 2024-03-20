"""
Test Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Role


def create_data(new={}):
    data_set = {
                'first_name': 'Mohamed',
                'last_name': 'zakaria',
                'email': 'momo@example.com',
                'password': 'Test123',
                'phone_number': '+201011111111',
                'role': 'CUSTOMER'
                }
    data_set.update(new)
    return data_set


class TestCustomUserModel(TestCase):
    """Testing the functionality of CustomUserModel"""
    def test_create_customer(self):
        customer_data = create_data()
        customer = get_user_model().objects.create_user(**customer_data)
        self.assertEqual(customer.role, Role.CUSTOMER)
        self.assertFalse(customer.is_superuser)
        self.assertFalse(customer.is_staff)
        self.assertTrue(customer.is_active)

    def test_create_tenant(self):
        tenant_data = create_data({'role': 'TENANT'})
        tenant = get_user_model().objects.create_user(**tenant_data)
        self.assertEqual(tenant.role, Role.TENANT)
        self.assertFalse(tenant.is_superuser)
        self.assertFalse(tenant.is_staff)
        self.assertTrue(tenant.is_active)

    def test_create_admin(self):
        admin_data = create_data({'role': 'ADMIN'})
        admin = get_user_model().objects.create_superuser(**admin_data)
        self.assertEqual(admin.role, Role.ADMIN)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_active)

    def test_create_staff(self):
        staff_data = create_data({'role': 'DESIGNER'})
        staff = get_user_model().objects.create_staff(**staff_data)
        self.assertEqual(staff.role, Role.DESIGNER)
        self.assertFalse(staff.is_superuser)
        self.assertTrue(staff.is_staff)
        self.assertTrue(staff.is_active)

    def test_create_no_email(self):
        user_data = create_data({'email': ''})
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(user_data)

    def test_create_no_password(self):
        user_data = create_data({'password': ''})
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(user_data)

    def test_slug_name(self):
        user_data = create_data()
        user = get_user_model().objects.create_user(**user_data)
        self.assertNotEqual('mohamed-khaled', user.slug_name)
        self.assertEqual('mohamed-zakaria', user.slug_name)

    def test_many_users_same_email(self):
        user_one = create_data()
        user_two = create_data()
        with self.assertRaises(Exception):
            get_user_model.objects.create_user(**user_one)
            get_user_model.objects.create_user(**user_two)

    def test_enter_phone_no_without_region(self):
        user_data = create_data({'phone_number': '01011111111'})
        user = get_user_model().objects.create_user(**user_data)
        self.assertEqual(user.phone_number, '+201011111111')
