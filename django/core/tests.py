from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

from core.models import Movie
from core.views import MovieList


class MovieListPaginationTestCase(TestCase):
    ACTIVE_PAGINATION_HTML = """
    <li class="page-item active">
    <a href="{}?page={}" class="page-link">{}</a>
    </li>"""

    def setUp(self):
        for n in range(15):
            Movie.objects.create(
                title='Title{}'.format(n),
                year=1990 + n,
                runtime=100,
            )

    def testFirstPage(self):
        movie_list_path = reverse('core:MovieList')  # 生成url
        request = RequestFactory().get(path=movie_list_path, )  # 生成reuqest get 请求
        response = MovieList.as_view()(request)  #get请求path
        self.assertEqual(200, response.status_code)  # 响应码为200
        self.assertTrue(response.context_data['is_paginated']) # 响应的值为is_paginated
        self.assertInHTML(
            self.ACTIVE_PAGINATION_HTML.format(movie_list_path, 1, 1),
            response.rendered_content
        )
