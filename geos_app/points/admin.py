from django.contrib import admin
from .models import PointsModel, LinesModel
from django.contrib.gis import forms



class PointsAdminForm(forms.ModelForm):
    geom = forms.PointField(widget=forms.OSMWidget(attrs={
            'display_raw': True, 'zoom':10}))

class PointsModelAdmin(admin.ModelAdmin):
    list_display = ["id", "obj_id" ,"city", "score", "geom"]
    form = PointsAdminForm


class LinesModelAdmin(admin.ModelAdmin):
    list_display = ['line_id', 'get_from_city', 'get_to_city']
    



admin.site.register(PointsModel, PointsModelAdmin)
admin.site.register(LinesModel, LinesModelAdmin)