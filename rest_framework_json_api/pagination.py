from rest_framework.response import Response
from rest_framework.compat import OrderedDict

try:
    from rest_framework.pagination import PageNumberPagination
    from rest_framework.utils.urls import (
        replace_query_param,
    )

    class JsonApiPageNumberPagination(PageNumberPagination):

        page_size = 10

        def get_paginated_response(self, data):
            return Response(OrderedDict([
                ('first', self.get_first_link()),
                ('last', self.get_last_link()),
                ('prev', self.get_previous_link()),
                ('next', self.get_next_link()),
                ('results', data)
            ]))

        def get_first_link(self):

            url = self.request.build_absolute_uri()
            page_number = 1
            return replace_query_param(url, self.page_query_param, page_number)

        def get_last_link(self):

            url = self.request.build_absolute_uri()
            page_number = self.page.paginator.num_pages
            return replace_query_param(url, self.page_query_param, page_number)
except ImportError:
    from rest_framework.pagination import (NextPageField, PreviousPageField,
                                           BasePaginationSerializer)
    from rest_framework import serializers
    from rest_framework.templatetags.rest_framework import replace_query_param

    class FirstPageField(serializers.Field):
        """
        Field that returns a link to the first page in paginated results.
        """
        page_field = 'page'

        def to_representation(self, value):
            page = 1
            request = self.context.get('request')
            url = request and request.build_absolute_uri() or ''
            return replace_query_param(url, self.page_field, page)

    class LastPageField(serializers.Field):
        """
        Field that returns a link to the last page in paginated results.
        """
        page_field = 'page'

        def to_representation(self, value):
            page = value.paginator.num_pages
            request = self.context.get('request')
            url = request and request.build_absolute_uri() or ''
            return replace_query_param(url, self.page_field, page)

    class JsonApiPaginationSerializer(BasePaginationSerializer):
        next = NextPageField(source='*')
        prev = PreviousPageField(source='*')
        first = FirstPageField(source='*')
        last = LastPageField(source='*')

        # total_results = serializers.Field(source='paginator.count')
        results_field = 'results'
