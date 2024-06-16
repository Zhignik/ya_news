from django.urls import reverse
import pytest
from news.models import Comment, News
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta

def test_news_count_on_home_page(client):
    for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        News.objects.create(
            title=f'Test News {i}',
            text=f'This is a test news {i}.'
        )
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    assert len(object_list) <= 10

def test_news_sorted_by_date(client):
    for i in range(5):
        News.objects.create(
            title=f'Test News {i}',
            text=f'This is a test news {i}.',
            date=datetime.today() - timedelta(days=i)
        )
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    assert all(object_list[i].date >= object_list[i+1].date for i in range(len(object_list)-1))

def test_comments_sorted_by_date(client, news, comment):
    url = reverse('news:detail', args=[news.id])
    response = client.get(url)
    assert 'news' in response.context
    news_obj = response.context['news']
    assert news_obj == news
    assert list(news_obj.comment_set.all()) == [comment]

def test_pages_contains_form(client, author_client, not_author_client, news):
    # Формируем URL.
    url = reverse('news:detail', args=[news.id])
    response_client = client.get(url)
    response_author = author_client.get(url)
    response_not_author = not_author_client.get(url)
    assert 'form' not in response_client.context
    assert 'form' in response_author.context
    assert 'form' in response_not_author.context

