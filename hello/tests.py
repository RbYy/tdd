from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from hello.views import index
from django.template.loader import render_to_string

# Create your tests here.


class HelloTest(TestCase):
    def test_url_root_resolver(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('index.html', request = request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_can_save_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = index(request)
        # print(response.content.decode())

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string('index.html', {
                       'new_item_text': 'A new list item'}, request = request)
        # print(expected_html)
        self.assertEqual(expected_html, response.content.decode())

