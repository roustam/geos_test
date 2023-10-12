from django.contrib.gis import admin
from .models import PointsModel, LinesModel
admin.site.register(PointsModel)
admin.site.register(LinesModel)
