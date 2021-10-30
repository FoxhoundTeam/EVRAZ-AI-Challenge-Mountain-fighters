from django.db import models
from src.base.centrifugo import Centrifugo

class Employee(models.Model):

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    tabel_code = models.CharField(max_length=128, null=True, blank=True)
    bio_photo = models.ImageField(null=True, blank=True)

class WorkShop(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=512, unique=True)
    comment = models.TextField(null=True, blank=True)


class Camera(models.Model):

    name = models.CharField(max_length=64)
    work_shop = models.ForeignKey(WorkShop, on_delete=models.PROTECT)
    code = models.CharField(max_length=256, unique=True)
    comment = models.TextField(null=True, blank=True)


class Frame(models.Model):

    photo = models.ImageField(upload_to='photos/')
    camera = models.ForeignKey(Camera, on_delete=models.PROTECT)
    dttm = models.DateTimeField()

    def save(self, *args, send_to_socket=False, **kwargs):
        from src.base.serializers import FrameSerializer
        super().save(*args, **kwargs)
        if send_to_socket:
            c = Centrifugo()
            c.send_model('updates', self, FrameSerializer)

class Violation(models.Model):
    frame = models.ForeignKey(Frame, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, send_to_socket=False, **kwargs):
        from src.base.serializers import ViolationSerializer
        super().save(*args, **kwargs)
        if send_to_socket:
            c = Centrifugo()
            c.send_model('updates', self, ViolationSerializer)


class AnalyzeResult(models.Model):

    frame = models.OneToOneField(Frame, on_delete=models.PROTECT, related_name='analyze')
    dttm = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()


class Setting(models.Model):

    recognition_model = models.CharField(max_length=256)
