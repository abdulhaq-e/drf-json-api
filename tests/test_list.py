"""Test list views

Includes success tests for creating resources by POST to the list view
Error tests are in test_errors.py
"""

from django.core.urlresolvers import reverse
from tests import models
from tests.serializers import PostSerializer
from tests.utils import dump_json
from tests.views import PersonViewSet
import pytest

pytestmark = pytest.mark.django_db


def test_empty_list(client):
    results = {
        "data": [],
    }

    response = client.get(reverse("post-list"))

    assert response.content == dump_json(results)


def test_single_item_list(client):
    models.Person.objects.create(name="test")

    results = {
        "data": [
            {
                "attributes": {
                    "name": "test"
                },
                "links": {
                    "self": "http://testserver/people/1/"
                },
                "id": "1",
                "type": "people"
            }
        ]
    }

    response = client.get(reverse("person-list"))

    assert response.content == dump_json(results)


def test_multiple_item_list(client):
    models.Person.objects.create(name="test")
    models.Person.objects.create(name="other")

    results = {
        "data": [
            {
                "attributes": {
                    "name": "test"
                },
                "links": {
                    "self": "http://testserver/people/1/"
                },
                "id": "1",
                "type": "people"
            },
            {
                "attributes": {
                    "name": "other"
                },
                "links": {
                    "self": "http://testserver/people/2/"
                },
                "id": "2",
                "type": "people"
            }
        ]
    }

    response = client.get(reverse("person-list"))

    assert response.content == dump_json(results)


def test_create_person_success(client):
    data = dump_json({
        "data": {
            "name": "Jason Api"
        }
    })
    results = {
        "data": {
            "id": "1",
            "type": "people",
            "links": {
                "self": "http://testserver/people/1/"
            },
            "attributes": {
                "name": "Jason Api"
            },
        },
    }

    response = client.post(
        reverse("person-list"), data=data,
        content_type="application/vnd.api+json")

    assert response.status_code == 201
    assert response.content == dump_json(results)
    assert response['content-type'] == 'application/vnd.api+json'
    person = models.Person.objects.get()
    assert person.name == 'Jason Api'


def test_create_post_success(client):
    author = models.Person.objects.create(name="The Author")

    data = dump_json({
        "data": {
            "type": "posts",
            "attributes": {
                "title": "This is the title",
            },
            "relationships": {
                "author": {
                    "data": {
                        "id": author.pk
                    }
                },
                "comments": {
                    "data": [],
                },
            },
        }
    })

    response = client.post(
        reverse("post-list"), data=data,
        content_type="application/vnd.api+json")
    assert response.status_code == 201
    assert response['content-type'] == 'application/vnd.api+json'

    post = models.Post.objects.get()
    results = {
        "data": {
            "attributes": {
                "title": "This is the title",
            },
            "id": str(post.pk),
            "type": "posts",
            "links": {
                "self": "http://testserver/posts/%s/" % post.pk,
            },
            "relationships": {
                "author": {
                    "data": {
                        "id": str(author.pk),
                        "type": "people"
                    }
                },
                "comments": {
                    "data": []
                }
            }
        },
    }

    assert response.content == dump_json(results)


def test_options(client):
    # DRF 3.x representation
    results = {
        "meta": {
            "actions": {
                "POST": {
                    "author": {
                        "choices": [],
                        "label": "Author",
                        "read_only": False,
                        "required": True,
                        "type": "field"
                    },
                    "comments": {
                        "choices": [],
                        "label": "Comments",
                        "read_only": False,
                        "required": True,
                        "type": "field"
                    },
                    "id": {
                        "label": "ID",
                        "read_only": True,
                        "required": False,
                        "type": "integer"
                    },
                    "title": {
                        "label": "Title",
                        "max_length": 100,
                        "read_only": False,
                        "required": True,
                        "type": "string"
                    },
                    "url": {
                        "label": "Url",
                        "read_only": True,
                        "required": False,
                        "type": "field"
                    }
                }
            },
            "description": "",
            "name": "Post List",
            "parses": ["application/vnd.api+json"],
            "renders": ["application/vnd.api+json"],
        }
    }

    # DRF 2.x representation - fields labels are lowercase, no choices
    ps = PostSerializer()
    if hasattr(ps, 'metadata'):
        results['meta']['actions']['POST'] = ps.metadata()

    import rest_framework
    version = rest_framework.__version__.split(".")

    # for DRF 3.0 compatibility.
    if int(version[0]) == 3 and int(version[1]) == 0:
        results['meta']['actions']['POST']['title'].pop('max_length', None)

    response = client.options(reverse("post-list"))
    assert response.status_code == 200
    assert response.content == dump_json(results)


def test_pagination(rf):
    models.Person.objects.create(name="test")

    import rest_framework
    version = rest_framework.__version__.split(".")

    # for DRF 3.0 compatibility.
    if int(version[0]) == 3 and int(version[1]) == 0:
        from rest_framework_json_api.pagination import (
            JsonApiPaginationSerializer)

        class PaginatedPersonViewSet(PersonViewSet):
            paginate_by = 10
            pagination_serializer_class = JsonApiPaginationSerializer
    else:
        from rest_framework_json_api.pagination import (
            JsonApiPageNumberPagination)

        class PaginatedPersonViewSet(PersonViewSet):
            pagination_class = JsonApiPageNumberPagination

    request = rf.get(
        reverse("person-list"), content_type="application/vnd.api+json")
    view = PaginatedPersonViewSet.as_view({'get': 'list'})
    response = view(request)
    response.render()

    assert response.status_code == 200, response.content

    results = {
        "data": [
            {
                "type": "people",
                "attributes": {
                    "name": "test",
                },
                "id": "1",
                "links": {
                    "self": "http://testserver/people/1/",
                },

            },
        ],
        "links": {
            "first": "http://testserver/people/?page=1",
            "last": "http://testserver/people/?page=1",
            "prev": None,
            "next": None
        },
    }
    assert response.content == dump_json(results)
