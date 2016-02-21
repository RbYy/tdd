from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
import hello.views
from django.template.loader import render_to_string

# Create your tests here.


class HelloTest(TestCase):
    def test_url_root_resolver(self):
        found = resolve('/')
        self.assertEqual(found.func, hello.views.index)

    def test_returns_correct_html(self):
        request = HttpRequest()
        response = hello.views.index(request)
        expected_html = render_to_string('index.html')
        self.assertEqual(expected_html, response.content.decode())

