import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from psqlextra.indexes import UniqueIndex


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        indexes = [
            UniqueIndex(fields=['name'], name='genre_names_idx'),
        ]

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full name'))

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        indexes = [
            models.Index(fields=['full_name'], name='person_full_names_idx'),
        ]

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class TypeChoice(models.TextChoices):
        movie = 1, _('movie')
        tv_show = 2, _('tv_show')
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True)
    file_path = models.TextField(_('file path'), blank=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[
                                    MinValueValidator(0),
                                    MaxValueValidator(100)
                                ])
    type = models.CharField(_('type'), choices=TypeChoice.choices, default=TypeChoice.movie)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    person = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        indexes = [
            models.Index(fields=['title', 'creation_date'], name='film_work_titles_creation_idx'),
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = [
            UniqueIndex(fields=['film_work_id', 'genre_id'], name='film_work_genre_idx'),
        ]


class PersonFilmwork(UUIDMixin):
    class RoleChoice(models.TextChoices):
        actor = 1, _('actor')
        writer = 2, _('writer')
        director = 3, _('director')
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), choices=RoleChoice.choices, default=RoleChoice.actor)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        indexes = [
            UniqueIndex(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_role_idx'),
        ]
