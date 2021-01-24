from django.core import validators
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import SmallIntegerField
from django.contrib.postgres.fields import ArrayField

from .constants import TABLE_FORMS, FORM_RECTANGULAR


class Table(models.Model):
    number_of_seats = models.PositiveSmallIntegerField(default=2)
    form = models.PositiveSmallIntegerField(choices=TABLE_FORMS, default=FORM_RECTANGULAR,
                                            help_text='Storing form as integer to save memory resources')
    first_point = ArrayField(models.IntegerField(), blank=True, default=list)
    second_point = ArrayField(models.IntegerField(), blank=True, default=list)
    height = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                      help_text='Unit of measurement - percent')
    width = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                     help_text='Unit of measurement - percent')

    @staticmethod
    def get_choice_object(object_id, choices):
        if object_id or isinstance(object_id, int):
            return {
                'id': object_id,
                'name': dict(choices)[object_id]
            }
        return None

    @property
    def object_form(self):
        return self.get_choice_object(self.form, TABLE_FORMS)

class Visitor(models.Model):
    name = models.CharField(max_length=225, default='Visitor', null=True)
    email = models.EmailField(null=True)

class Booking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    date = models.DateField()