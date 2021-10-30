from django.contrib import admin
from src.base.models import Employee, Camera, Frame, Violation, AnalyzeResult, Setting

admin.site.register(Employee)
admin.site.register(Camera)
admin.site.register(Frame)
admin.site.register(Violation)
admin.site.register(AnalyzeResult)
admin.site.register(Setting)
