from django.db import models


class Classes(models.Model):
    Name = models.CharField(max_length=32)
    Organic = models.IntegerField()


class Colors(models.Model):
    Name = models.CharField(max_length=32)


class Chemicals(models.Model):
    Name = models.CharField(max_length=32)
    Class = models.ForeignKey(Classes, on_delete=models.PROTECT)
    Color = models.ForeignKey(Colors, on_delete=models.PROTECT)

