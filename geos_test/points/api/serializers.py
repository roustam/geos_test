from rest_framework import serializers
from points.models import PointsModel, LinesModel
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class LineNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinesModel
        fields = ['from_point', 'to_point']


class LocationSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PointsModel
        many = True
        geo_field = "geom"
        fields = ('id', 'score', 'obj_id')

class LocationSerializerList(GeoFeatureModelSerializer):

    class Meta:
        model = PointsModel
        geo_field = "geom"
        fields = ('id', 'score', 'obj_id')

