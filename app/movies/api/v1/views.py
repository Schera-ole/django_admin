from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Filmwork.objects.values('id', 'title', 'description', 'creation_date', 'rating', 'type').annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg('personfilmwork__person__full_name', distinct=True, filter=Q(
                    personfilmwork__role=PersonFilmwork.RoleChoice.actor
            )),
            directors=ArrayAgg('personfilmwork__person__full_name', distinct=True, filter=Q(
                personfilmwork__role=PersonFilmwork.RoleChoice.director
            )),
            writers=ArrayAgg('personfilmwork__person__full_name', distinct=True, filter=Q(
                personfilmwork__role=PersonFilmwork.RoleChoice.writer
            ))
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = list(self.get_queryset())
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        previous_page = None if page.number == 1 else page.previous_page_number()
        next_page = None if page.number == paginator.num_pages else page.next_page_number()
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': previous_page,
            'next': next_page,
            'results': queryset,
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.object
