import pytest

from django.test.client import Client
from django.utils import timezone
from django.conf import settings
from news.models import Comment, News



@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):  
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Test News',
        text='This is a test news content.',
        date=timezone.now().date()
    )
    return news
@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='This is a test comment.',
        created=timezone.now()
    )

@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
    }