"""Regression checks using Flask's test client and isolated temporary JSON files."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import data
from app import app
from logic import build_report


class CafeTests(unittest.TestCase):
    """Exercise ordering behavior without consuming the demonstration's inventory."""

    def setUp(self):
        """Create a fresh data path and client for each test; return nothing."""
        self.folder = tempfile.TemporaryDirectory()
        self.original_file = data.DATA_FILE
        data.DATA_FILE = Path(self.folder.name) / 'orders.json'
        app.config.update(TESTING=True, SECRET_KEY='test-only-key')
        self.client = app.test_client()

    def tearDown(self):
        """Restore the original storage path and delete test files; return nothing."""
        data.DATA_FILE = self.original_file
        self.folder.cleanup()

    def add(self, item='1', quantity='1'):
        """Submit an add-item request and return its final HTML response."""
        return self.client.post('/add-to-cart', data={'item_id': item, 'quantity': quantity}, follow_redirects=True)

    def checkout(self, **settings):
        """Submit checkout settings and return the redirect or error response."""
        return self.client.post('/checkout', data=settings)

    def test_empty_cart(self):
        """Empty checkout must not save an order."""
        response = self.client.post('/checkout', follow_redirects=True)
        self.assertIn(b'Your cart is empty', response.data)
        self.assertEqual(data.load_data()['orders'], [])

    def test_bad_quantities(self):
        """Reject zero, negative, decimal, huge, nonnumeric, and missing additions."""
        for quantity in ['0', '-1', '1.5', '9' * 5000, 'coffee', '', '11']:
            with self.subTest(quantity=quantity[:20]):
                self.assertEqual(self.add(quantity=quantity).status_code, 200)
                with self.client.session_transaction() as browser:
                    self.assertEqual(browser.get('cart', {}), {})
        self.assertEqual(self.client.post('/add-to-cart', follow_redirects=True).status_code, 200)
        self.assertEqual(self.client.post('/update-cart', follow_redirects=True).status_code, 200)
        self.assertEqual(self.client.post('/remove-from-cart', follow_redirects=True).status_code, 200)
        self.assertIn(b'Choose an existing', self.add(item='bad').data)

    def test_sold_out_and_stock_limit(self):
        """Sold-out and over-stock additions are refused; accumulated limits hold."""
        self.assertIn(b'sold out', self.add('3').data)
        self.assertIn(b'Only 2', self.add('7', '3').data)
        self.add('1', '6')
        self.assertIn(b'limit is 10', self.add('1', '5').data)
        with self.client.session_transaction() as browser:
            self.assertEqual(browser['cart'], {'1': 6})

    def test_update_and_remove(self):
        """Updates reject invalid quantities and zero removes an existing item."""
        self.add()
        for quantity in ['-1', '1.1', 'abc', '11', '9' * 5000]:
            self.client.post('/update-cart', data={'item_id': '1', 'quantity': quantity})
            with self.client.session_transaction() as browser:
                self.assertEqual(browser['cart'], {'1': 1})
        self.client.post('/update-cart', data={'item_id': '1', 'quantity': '0'})
        with self.client.session_transaction() as browser:
            self.assertEqual(browser['cart'], {})
        self.add()
        self.client.post('/remove-from-cart', data={'item_id': 'bad'})
        self.client.post('/remove-from-cart', data={'item_id': '1'})
        with self.client.session_transaction() as browser:
            self.assertEqual(browser['cart'], {})

    def test_budget(self):
        """Reject overspending and malformed limits; an exact budget is allowed."""
        self.add()
        response = self.client.post('/checkout', data={'budget': '1'}, follow_redirects=True)
        self.assertIn(b'Budget exceeded', response.data)
        self.assertEqual(len(data.load_data()['orders']), 0)
        self.assertIn(b'Budget remaining: -$3.91', response.data)
        for budget in ['-1', '1.234', 'abc', '1e2']:
            self.assertEqual(self.checkout(budget=budget).status_code, 400)
        self.assertEqual(self.checkout(budget='4.91').status_code, 302)
        self.assertEqual(len(data.load_data()['orders']), 1)

    def test_delivery_discount_and_instructions(self):
        """Fees, discount rounding, instructions, and pickup totals persist correctly."""
        self.add()
        self.assertEqual(self.checkout(discount_code='bad').status_code, 400)
        self.assertEqual(self.checkout(fulfillment='unknown').status_code, 400)
        self.assertEqual(self.checkout(instructions='x' * 301).status_code, 400)
        self.assertEqual(data.load_data()['orders'], [])
        self.checkout(fulfillment='delivery', discount_code='cafe10', instructions='Extra hot')
        order = data.load_data()['orders'][0]
        self.assertEqual([order[k] for k in ['subtotal', 'discount', 'tax', 'delivery_fee', 'total']], [459, 46, 29, 399, 841])
        self.assertEqual(order['instructions'], 'Extra hot')
        self.add()
        self.checkout(fulfillment='pickup')
        self.assertEqual(data.load_data()['orders'][1]['total'], 491)
        self.assertEqual(data.load_data()['orders'][1]['delivery_fee'], 0)

    def test_preview_settings(self):
        """Saving settings changes the preview and keeps user entries visible."""
        self.add()
        response = self.client.post('/cart-settings', data={'fulfillment': 'delivery', 'budget': '20', 'instructions': 'Hi'}, follow_redirects=True)
        self.assertIn(b'action="/checkout"', response.data)
        self.assertIn(b'formaction="/cart-settings"', response.data)
        self.assertIn(b'$8.90', response.data)
        self.assertIn(b'$11.10', response.data)
        self.assertIn(b'Hi', response.data)
        self.assertEqual(data.load_data()['orders'], [])

    def test_checkout_rechecks_stock(self):
        """A second customer's purchase can exhaust inventory before checkout."""
        self.add('7', '2')
        other_customer = app.test_client()
        other_customer.post('/add-to-cart', data={'item_id': '7', 'quantity': '2'})
        other_customer.post('/checkout')
        response = self.client.post('/checkout', follow_redirects=True)
        self.assertIn(b'no longer has enough stock', response.data)
        self.assertEqual(len(data.load_data()['orders']), 1)
        self.assertEqual(data.load_data()['menu'][6]['stock'], 0)

    def test_receipt_refresh_and_restart(self):
        """Receipt GET is read-only and a fresh Python process sees saved stock/orders."""
        self.add()
        response = self.checkout()
        self.assertEqual(response.location, '/receipt/1')
        first = self.client.get(response.location)
        second = self.client.get(response.location)
        self.assertEqual(first.data, second.data)
        self.assertEqual(len(data.load_data()['orders']), 1)
        environment = dict(os.environ, CAFE_DATA_FILE=str(data.DATA_FILE))
        result = subprocess.check_output([os.sys.executable, '-c',
            'from data import load_data; s=load_data(); print(s["menu"][0]["stock"], len(s["orders"]))'], env=environment, text=True)
        self.assertEqual(result.strip(), '49 1')
        self.assertEqual(app.test_client().get('/receipt/1').status_code, 200)
        self.assertEqual(self.client.get('/receipt/999').status_code, 404)
        self.client.get('/receipt')
        self.assertEqual(len(data.load_data()['orders']), 1)

    def test_report_filters_and_sort(self):
        """Date/category filters and both sort choices affect the actual report data."""
        self.add('1', '1')
        self.add('6', '2')
        self.add('5', '4')
        self.checkout()
        state = data.load_data()
        for sort in ['revenue', 'quantity']:
            report, error = build_report(state['orders'], state['menu'], {'sort': sort})
            self.assertIsNone(error)
            expected = 'Black Coffee' if sort == 'quantity' else 'Blueberry Muffin'
            self.assertEqual(report['sales'][0]['name'], expected)
            self.assertEqual(report['best']['quantity'], 4)
            self.assertEqual(self.client.get('/report?sort=' + sort).status_code, 200)
        report, _ = build_report(state['orders'], state['menu'], {'category': 'Drinks'})
        self.assertEqual(len(report['sales']), 2)
        self.assertEqual(report['sales'][0]['name'], 'Black Coffee')
        self.assertEqual(report['revenue'], state['orders'][0]['total'])
        day = state['orders'][0]['timestamp'][:10]
        report, _ = build_report(state['orders'], state['menu'], {'start': day, 'end': day})
        self.assertEqual(len(report['orders']), 1)
        report, _ = build_report(state['orders'], state['menu'], {'end': '2000-01-01'})
        self.assertEqual(report['orders'], [])
        for query in ['start=bad', 'start=2026-02-30', 'start=2027-01-01&end=2020-01-01', 'category=Other', 'sort=bad']:
            self.assertEqual(self.client.get('/report?' + query).status_code, 400)

    def test_navigation_assets_and_help(self):
        """All main links/assets load and unknown questions receive a helpful answer."""
        for path in ['/', '/menu', '/cart', '/report', '/story', '/help', '/contact']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertNotIn(b'href="#"', response.data)
                self.assertNotIn(b'src="script.js"', response.data)
        for asset in Path('static').rglob('*'):
            if asset.is_file() and not asset.name.startswith('.'):
                response = self.client.get('/' + asset.as_posix())
                self.assertEqual(response.status_code, 200)
                response.close()
        response = self.client.post('/help', data={'question': 'purple zebras?'})
        self.assertIn(b'Try asking about budget', response.data)
        response = self.client.post('/help', data={'question': 'What is my budget?'})
        self.assertIn(b'Set an optional budget', response.data)
        response = self.client.post('/help', data={'question': '<script>alert(1)</script>'})
        self.assertNotIn(b'<script>alert(1)</script>', response.data)

    def test_storage_failure_keeps_cart(self):
        """A failed save must not reduce stock or clear the customer's cart."""
        self.add()
        with patch('logic.save_data', side_effect=OSError('disk full')):
            response = self.client.post('/checkout', follow_redirects=True)
        self.assertIn(b'Could not save', response.data)
        self.assertEqual(data.load_data()['menu'][0]['stock'], 50)
        with self.client.session_transaction() as browser:
            self.assertEqual(browser['cart'], {'1': 1})

    def test_category_and_search_combine(self):
        """Category navigation retains search and filters its matches independently."""
        response = self.client.get('/menu?category=Drinks&q=coffee')
        self.assertIn(b'Black Coffee', response.data)
        self.assertNotIn(b'Blueberry Muffin', response.data)
        self.assertIn(b'name="category" value="Drinks"', response.data)
        self.assertIn(b'No items found.', self.client.get('/menu?category=Food&q=coffee').data)
        self.assertIn(b'Blueberry Muffin', self.client.get('/menu?category=invalid').data)
        # Legacy search-by-category links still work.
        self.assertNotIn(b'Blueberry Muffin', self.client.get('/menu?q=Drinks').data)

    def test_add_feedback_and_browsing_context(self):
        """Additions keep the active menu context and identify what was added."""
        response = self.client.post('/add-to-cart', data={
            'item_id': '1', 'quantity': '2', 'category': 'Drinks', 'q': 'latte'})
        self.assertIn('category=Drinks', response.location)
        self.assertIn('q=latte', response.location)
        page = self.client.get(response.location)
        self.assertIn('Added 2 × Latte to your order.'.encode(), page.data)
        self.assertIn(b'aria-label="2 items"', page.data)
        error = self.add('3')
        self.assertIn(b'class="notice error"', error.data)
        self.assertIn(b'role="alert"', error.data)

    def test_remove_button_and_empty_checkout(self):
        """The inline removal action preserves its contract; empty carts hide checkout."""
        self.add()
        page = self.client.get('/cart')
        self.assertIn(b'formaction="/remove-from-cart" formnovalidate', page.data)
        self.assertIn(b'data-settings-form', page.data)
        self.client.post('/remove-from-cart', data={'item_id': '1'})
        empty = self.client.get('/cart')
        self.assertIn(b'Your cart is empty', empty.data)
        self.assertNotIn(b'Place demo order', empty.data)


if __name__ == '__main__':
    unittest.main()
