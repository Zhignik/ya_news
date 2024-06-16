from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from django.urls import reverse
from news.models import Comment
from news.forms import BAD_WORDS, WARNING

def test_anonymous_user_cant_comment(client, news, form_data):
    url = reverse('news:detail', args=[news.id])
    initial_comment_count = Comment.objects.count()
    response = client.post(url, form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)

    assert Comment.objects.count() == initial_comment_count


def test_authenticated_user_can_comment(author_client, author, news, form_data):
    url = reverse('news:detail', args=[news.id])
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_comment_with_bad_words_not_published(author_client, news):
    url = reverse('news:detail', args=[news.id])
    form_data = {
        'text': f'Text plus {BAD_WORDS[0]}',
    }
    response = author_client.post(url, data=form_data)
    form = response.context['form']
    assert form.errors
    assert WARNING in form.errors['text']
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.FOUND
    comment.refresh_from_db()
    assert comment.text == form_data['text']

def test_author_can_delete_comment(author_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    author_client.post(url)
    assert Comment.objects.count() == 0

def test_other_user_cant_edit_comment(not_author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text

def test_other_user_cant_delete_note(not_author_client, comment):
    url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
