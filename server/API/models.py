from django.db import models


class Stove(models.Model):
    date = models.DateField()
    stoves_num = models.IntegerField(default=0)
    work_num = models.IntegerField()
    work_time = models.FloatField()

    def __str__(self):
        return f'{self.date, self.stoves_num, self.work_num, self.work_time}'

class District(models.Model):
    district = models.CharField(max_length=255, default=None)
    count = models.IntegerField()

    def str(self):
        return f'{self.district, self.count}'
