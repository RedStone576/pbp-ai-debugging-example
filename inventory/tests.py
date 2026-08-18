from django.test import TestCase, Client
from django.urls import reverse
from inventory.models import Item

class InventoryAjaxTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_url = reverse('inventory:add_item_ajax')

    def test_add_item_ajax_success(self):
        """Valid submission should create item and return HTTP 201 Created."""
        payload = {
            'name': 'Mouse Wireless',
            'price': 150000,
            'description': 'Mouse ergonomis 2.4GHz'
        }
        response = self.client.post(self.add_url, payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Item.objects.count(), 1)
        
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['name'], 'Mouse Wireless')

    def test_add_item_ajax_empty_fields_returns_400(self):
        """Empty form submission must return HTTP 400 Bad Request with field validation errors."""
        payload = {
            'name': '',
            'price': '',
            'description': ''
        }
        response = self.client.post(self.add_url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Item.objects.count(), 0)
        
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('name', data['errors'])
        self.assertIn('price', data['errors'])

    def test_add_item_ajax_invalid_price_type(self):
        """Non-numeric price submission must trigger Django validation error and return HTTP 400."""
        payload = {
            'name': 'Keyboard Mechanical',
            'price': 'bukan_angka',
            'description': 'Switch Blue'
        }
        response = self.client.post(self.add_url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Item.objects.count(), 0)
        
        data = response.json()
        self.assertIn('price', data['errors'])
