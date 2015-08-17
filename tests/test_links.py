# from django.core.urlresolvers import reverse
# from tests import models
# from tests.utils import dump_json
# import pytest

# pytestmark = pytest.mark.django_db


# def test_single_links(client):
#     author = models.Person.objects.create(name="test")
#     post = models.Post.objects.create(author=author, title="Test post title.")
#     models.Comment.objects.create(post=post, body="Some text for testing.")

#     results = {
#         "links": {
#             "comments.post": {
#                 "href": "http://testserver/posts/{comments.post}/",
#                 "type": "posts",
#             },
#         },
#         "data": [
#             {
#                 "id": "1",
#                 "type": "comments"
#                 "attributes": {
#                     "body": "Some text for testing.",
#                 },
#                 "links": {
#                     "self": "http://testserver/comments/1/",
#                 },
#                 "relationships": {
#                     "post": {
#                         "data": {"id": "1", "type": "posts"}
#                     }
#                 }
#             },
#         ],
#     }

#     response = client.get(reverse("comment-list"))
#     print response.content
#     assert response.content == dump_json(results)


# def test_multiple_links(client, url_name='post-list'):
#     author = models.Person.objects.create(name="test")
#     post = models.Post.objects.create(author=author, title="Test post title")
#     models.Comment.objects.create(post=post, body="Test comment one.")
#     models.Comment.objects.create(post=post, body="Test comment two.")

#     results = {
#         "links": {
#             "posts.author": {
#                 "href": "http://testserver/people/{posts.author}/",
#                 "type": "people",
#             },
#             "posts.comments": {
#                 "href": "http://testserver/comments/{posts.comments}/",
#                 "type": "comments",
#             }
#         },
#         "posts": [
#             {
#                 "id": "1",
#                 "title": "Test post title",
#                 "href": "http://testserver/posts/1/",
#                 "links": {
#                     "author": "1",
#                     "comments": ["1", "2"]
#                 }
#             },
#         ],
#     }

#     response = client.get(reverse(url_name))

#     assert response.content == dump_json(results)


# def test_multiple_links_with_namespaced_url(client):
#     test_multiple_links(client, url_name='n1:post-list')


# def test_pk_related(client):
#     author = models.Person.objects.create(name="test")
#     post = models.Post.objects.create(author=author, title="Test post title.")
#     models.Comment.objects.create(post=post, body="Some text for testing.")

#     results = {
#         "links": {
#             "comments.post": {
#                 "type": "posts",
#             },
#         },
#         "comments": [
#             {
#                 "id": "1",
#                 "body": "Some text for testing.",
#                 "href": "http://testserver/comments/1/",
#                 "links": {
#                     "post": "1",
#                 },
#             },
#         ],
#     }

#     response = client.get(reverse("pk-comment-list"))

#     assert response.content == dump_json(results)
