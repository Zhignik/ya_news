import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects



def test_home_availability_for_anonymous_user(client):
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_news_detail_page_availability_for_anonymous_user(client, news):
    # Получаем URL страницы этой новости
    url = reverse('news:detail', args=[news.id])
    # Выполняем GET-запрос к этому URL
    response = client.get(url)
    # Проверяем, что статус ответа HTTP 200 (OK)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    # Предварительно оборачиваем имена фикстур 
    # в вызов функции pytest.lazy_fixture().
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_pages_availability_for_different(parametrized_client,expected_status, name, comment):
    url = reverse(name, args = [comment.id])
    response = parametrized_client.get(url)
    assert response.status_code == expected_status

@pytest.mark.parametrize(
    'name',
    ('users:login', 'users:logout', 'users:signup')
)
# Указываем имя изменяемого параметра в сигнатуре теста.
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)

def test_redirects(client, name, comment):
    login_url = reverse('users:login')
    # Теперь не надо писать никаких if и можно обойтись одним выражением.
    url = reverse(name, args= [comment.id])
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


