from django.core.urlresolvers import reverse
from tests import models
from tests.utils import dump_json, parse_json
import pytest

pytestmark = pytest.mark.django_db


def test_single_linked(client):
    author = models.Person.objects.create(name="test")
    post = models.Post.objects.create(
        author=author, title="One amazing test post.")
    models.Comment.objects.create(
        post=post, body="This is a test comment.")

    results = {
        "data": [
            {
                "id": "1",
                "type": "comments",
                "attributes": {
                    "body": "This is a test comment.",
                },
                "links": {
                    "self": "http://testserver/comments/1/",
                },
                "relationships": {
                    "post": {
                        "data": {"id": "1", "type": "posts"}
                    }
                }
            },
        ],
        # "links": {
        #     "comments.post": {
        #         "href": "http://testserver/posts/{comments.post}/",
        #         "type": "posts",
        #     },
        # },
        "included": [
            {
                "id": "1",
                "type": "posts",
                "attributes": {
                    "title": "One amazing test post.",
                },
                "links": {
                    "self": "http://testserver/posts/1/",
                }
            },
        ],
    }

    response = client.get(reverse("nested-comment-list"))
    assert response.content == dump_json(results)


def test_multiple_linked(client):
    author = models.Person.objects.create(name="test")
    post = models.Post.objects.create(
        author=author, title="One amazing test post.")
    models.Comment.objects.create(
        post=post, body="This is a test comment.")
    models.Comment.objects.create(
        post=post, body="One more comment.")

    results = {
        "data": [
            {
                "id": "1",
                "type": "posts",
                "attributes": {
                    "title": "One amazing test post.",
                },
                "links": {
                    "self": "http://testserver/posts/1/",
                },
                "relationships": {
                    "author": {
                        "data": {"id": "1", "type": "people"}
                    },
                    "comments": {
                        "data": [{"id": "1", "type": "comments"},
                                 {"id": "2", "type": "comments"}
                        ],
                    },
                }
            },
        ],
        # "links": {
        #     "posts.author": {
        #         "href": "http://testserver/people/{posts.author}/",
        #         "type": "people",
        #     },
        #     "posts.comments": {
        #         "href": "http://testserver/comments/{posts.comments}/",
        #         "type": "comments",
        #     }
        # },
        "included": [
            {
                "id": "1",
                "type": "comments",
                "links": {
                    "self": "http://testserver/comments/1/",
                },
                "attributes": {
                    "body": "This is a test comment.",
                },
            },
            {
                "id": "2",
                "type": "comments",
                "links": {
                    "self": "http://testserver/comments/2/",
                },
                "attributes": {
                    "body": "One more comment.",
                },
            },
        ],
    }

    response = client.get(reverse("nested-post-list"))
    print response.content, dump_json(results),
    assert response.content == dump_json(results)


def test_multiple_root_entities_linked(client):
    author = models.Person.objects.create(name="test")
    post = models.Post.objects.create(
        author=author, title="One amazing test post.")
    post2 = models.Post.objects.create(
        author=author, title="A second amazing test post.")
    models.Comment.objects.create(
        post=post, body="This is a test comment.")
    models.Comment.objects.create(
        post=post, body="One more comment.")
    models.Comment.objects.create(
        post=post2, body="One last comment.")

    results = {
        "data": [
            {
                "id": "1",
                "type": "posts",
                "links": {
                    "self": "http://testserver/posts/1/"
                },
                "attributes": {
                    "title": "One amazing test post."
                },
                "relationships": {
                    "author": {
                        "data": {"id": "1", "type": "people"}
                    },
                    "comments": {
                        "data": [{"id": "1", "type": "comments"},
                                 {"id": "2", "type": "comments"}]
                    },
                },
            },
            {
                "id": "2",
                "type": "posts",
                "links": {
                    "self": "http://testserver/posts/2/"
                },
                "attributes": {
                    "title": "A second amazing test post."
                },
                "relationships": {
                    "author": {
                        "data": {"id": "1", "type": "people"}
                    },
                    "comments": {
                        "data": [{"id": "3", "type": "comments"}],
                    },
                },
            },
        ],
        # "links": {
        #     "posts.author": {
        #         "href": "http://testserver/people/{posts.author}/",
        #         "type": "people",
        #     },
        #     "posts.comments": {
        #         "href": "http://testserver/comments/{posts.comments}/",
        #         "type": "comments",
        #     }
        # },
        "included": [
            {
                "id": "1",
                "type": "comments",
                "attributes": {
                    "body": "This is a test comment.",
                },
                "links": {
                    "self": "http://testserver/comments/1/",
                },
            },
            {
                "id": "2",
                "type": "comments",
                "attributes": {
                    "body": "One more comment.",
                },
                "links": {
                    "self": "http://testserver/comments/2/",
                },
            },
            {
                "id": "3",
                "type": "comments",
                "attributes": {
                    "body": "One last comment.",
                },
                "links": {
                    "self": "http://testserver/comments/3/",
                },
            },
        ]
    }
    response = client.get(reverse("nested-post-list"))

    assert response.content == dump_json(results)
