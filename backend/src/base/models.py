from django.db import models

class Employee(models.Model):

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    tabel_code = models.CharField(max_length=128, null=True, blank=True)
    bio_photo = models.ImageField(null=True, blank=True)


class Camera(models.Model):

    name = models.CharField(max_length=64)
    code = models.CharField(max_length=256, unique=True)
    comment = models.TextField(null=True, blank=True)


class Frame(models.Model):

    photo = models.ImageField('photos/')
    camera = models.ForeignKey(Camera, on_delete=models.PROTECT)
    dttm = models.DateTimeField()

class Violation(models.Model):
    frame = models.ForeignKey(Frame, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, blank=True)


class AnalyzeResult(models.Model):

    frame = models.OneToOneField(Frame, on_delete=models.PROTECT, related_name='analyze')
    dttm = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()


class Setting(models.Model):

    recognition_model = models.CharField(max_length=256)
