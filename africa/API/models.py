from django.db import models


class Stove(models.Model):
    number = models.IntegerField(default=0)
    date = models.DateField()
    amount_of_stoves = models.IntegerField()
    average_number_of_hours = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.number, self.date, self.amount_of_stoves, self.average_number_of_hours}'

