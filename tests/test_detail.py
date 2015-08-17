from django.core.urlresolvers import reverse
from tests import models
from tests.utils import dump_json, parse_json
import pytest

pytestmark = pytest.mark.django_db


def test_object(client):
    models.Person.objects.create(name="test")

    results = {
        "data": {
            "id": "1",
            "type": "people",
            "attributes":
            {
                "name": "test"
            },
            "links": {
                "self": "http://testserver/people/1/",
            }
        }
    }

    response = client.get(reverse("person-detail", args=[1]))
    assert response.content == dump_json(results)


def test_object_with_optional_links(client):
    models.Person.objects.create(name="test")

    results = {
        "data": {
            "id": "1",
            "type": "people",
            "attributes": {
                "name": "test"
            },
            "relationships": {
                "favorite_post": {
                    "data": None
                },
                "liked_comments": {
                    "data": []
                }
            },
            "links": {
                "self": "http://testserver/people/1/",
            },
        },
    }

    response = client.get(reverse("people-full-detail", args=[1]))

    assert response.content == dump_json(results)


def test_update_attribute(client):
    models.Person.objects.create(name="test")

    data = dump_json({
        "data": {
            "attributes": {
                "name": "new test",
            },
        },
    })

    results = {
        "data": {
            "id": "1",
            "type": "people",
            "attributes": {
                "name": "new test",
            },
            "relationships": {
                "favorite_post": {
                    "data": None
                },
                "liked_comments": {
                    "data": []
                }
            },
            "links": {
                "self": "http://testserver/people/1/",
            },
        },
    }

    response = client.patch(
        reverse("people-full-detail", args=[1]), data,
        content_type="application/vnd.api+json")

    assert response.content == dump_json(results)


def test_update_to_one_link(client):
    models.Person.objects.create(name="test")
    author = models.Person.objects.create(name="author")
    post = models.Post.objects.create(title="The Post", author=author)

    data = dump_json({
        "data": {
            "attributes": {
                "name": "test"
                },
            "relationships": {
                "favorite_post": {
                    "data": {
                        "type": "posts",
                        "id": str(post.pk),
                    },
                },
            },
        },
    })
    results = {
        "data": {
            "id": "1",
            "type": "people",
            "attributes": {
                "name": "test"
            },
            "links": {
                "self": "http://testserver/people/1/",
            },
            "relationships": {
                "favorite_post": {
                    "data": {
                        "type": "posts",
                        "id": str(post.pk),
                    }
                },
                "liked_comments": {
                    "data": [],
                },
            },
        },
    }

    response = client.patch(
        reverse("people-full-detail", args=[1]), data,
        content_type="application/vnd.api+json")

    assert response.content == dump_json(results)


def test_update_to_many_link(client):
    models.Person.objects.create(name="test")
    author = models.Person.objects.create(name="author")
    post = models.Post.objects.create(title="The Post", author=author)
    comment1 = models.Comment.objects.create(body="Comment 1", post=post)
    comment2 = models.Comment.objects.create(body="Comment 2", post=post)

    data = dump_json({
        "data": {
            "attributes": {
                "name": "test",
            },
            "relationships": {
                "favorite_post": {
                    "data": None
                },
                "liked_comments": {
                    "data": [
                        {
                            "type": "comments",
                            "id": str(comment1.pk),
                        },
                        {
                            "type": "comments",
                            "id": str(comment2.pk),
                        },
                    ],
                },
            },
        },
    })
    results = {
        "data": {
            "id": "1",
            "type": "people",
            "attributes": {
                "name": "test"
            },
            "links": {
                "self": "http://testserver/people/1/"
            },
            "relationships": {
                "favorite_post": {
                    "data": None,
                },
                "liked_comments": {
                    "data": [
                        {
                            "type": "comments",
                            "id": str(comment1.pk),
                        },
                        {
                            "type": "comments",
                            "id": str(comment2.pk),
                        },
                    ],
                },
            },
        },
    }

    response = client.put(
        reverse("people-full-detail", args=[1]), data,
        content_type="application/vnd.api+json")

    assert response.content == dump_json(results)


def test_object_with_pk_links(client):
    models.Person.objects.create(name="test")

    results = {
        "data": {
            "id": "1",
            "type": "people",
            "attributes": {
                "name": "test"
            },
            "links": {
                "self": "http://testserver/people/1/",
            },
            "relationships": {
                "favorite_post": {
                    "data": None,
                },
                "liked_comments": {
                    "data": [],
                }
            }
        }
    }

    response = client.get(reverse("pk-people-full-detail", args=[1]))

    assert response.content == dump_json(results)


def test_update_pk_attribute(client):
    models.Person.objects.create(name="test")

    data = dump_json({
        "data": {
            "type": "people",
            "attributes": {
                "name": "new test"
            },
            "relationships": {
                "favorite_post": {
                    "data": None,
                },
                "liked_comments": {
                    "data": [],
                },
            },
        },
    })

    results = {
        "data": {
            "id": "1",
            "type": "people",
            "attributes": {
                "name": "new test"
            },
            "links": {
                "self": "http://testserver/people/1/"
            },
            "relationships": {
                "favorite_post": {
                    "data": None,
                },
                "liked_comments": {
                    "data": [],
                },
            },
        },
    }

    response = client.patch(
        reverse("pk-people-full-detail", args=[1]), data,
        content_type="application/vnd.api+json")

    assert response.content == dump_json(results)


def test_update_to_one_pk_link(client):
    models.Person.objects.create(name="test")
    author = models.Person.objects.create(name="author")
    post = models.Post.objects.create(title="The Post", author=author)

    data = dump_json({
        "data": {
            "attributes": {
                "name": "test"
            },
            "type": "people",
            "relationships": {
                "favorite_post": {
                    "data": {
                        "type": "posts",
                        "id": str(post.pk),
                    }
                },
                "liked_comments": {
                    "data": [],
                },
            },
        },
    })
    results = {
        "data": {
            "id": "1",
            "type": "people",
            "attributes": {
                "name": "test"
            },
            "links": {
                "self": "http://testserver/people/1/"
            },
            "relationships": {
                "favorite_post": {
                    "data": {
                        "type": "posts",
                        "id": str(post.pk),
                    },
                },
                "liked_comments": {
                    "data": [],
                },
            },
        },
    }

    response = client.put(
        reverse("pk-people-full-detail", args=[1]), data,
        content_type="application/vnd.api+json")

    assert response.content == dump_json(results)


def test_update_to_many_pk_link(client):
    models.Person.objects.create(name="test")
    author = models.Person.objects.create(name="author")
    post = models.Post.objects.create(title="The Post", author=author)
    comment1 = models.Comment.objects.create(body="Comment 1", post=post)
    comment2 = models.Comment.objects.create(body="Comment 2", post=post)

    data = dump_json({
        "data": {
            "attributes": {
                "name": "test"
            },
            "type": "people",
            "relationships": {
                "favorite_post": {
                    "data": None,
                },
                "liked_comments": {
                    "data": [
                        {
                            "type": "comments",
                            "id": str(comment1.pk),
                        },
                        {
                            "type": "comments",
                            "id": str(comment2.pk),
                        },
                    ],
                },
            },
        },
    })
    results = {
        "data": {
            "id": "1",
            "type": "people",
            "attributes": {
                "name": "test"
            },
            "links": {
                "self": "http://testserver/people/1/"
            },
            "relationships": {
                "favorite_post": {
                    "data": None,
                },
                "liked_comments": {
                    "data": [
                        {
                            "type": "comments",
                            "id": str(comment1.pk),
                        },
                        {
                            "type": "comments",
                            "id": str(comment2.pk),
                        },
                    ],
                },
            },
        },
    }

    response = client.put(
        reverse("pk-people-full-detail", args=[1]), data,
        content_type="application/vnd.api+json")

    assert response.content == dump_json(results)
