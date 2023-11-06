from django.contrib.gis.db import models

class PointsModel(models.Model):
    id=models.AutoField(primary_key=True, unique=True)
    obj_id = models.IntegerField(default=0)
    geom = models.PointField()
    score = models.IntegerField()
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.city
    
    def get_city_name(self):
        return self.city

class LinesModel(models.Model):
    line_id = models.AutoField(primary_key=True, unique=True)
    from_point = models.ForeignKey(PointsModel,
                                      on_delete=models.CASCADE, related_name='from_point'
                                      )
    to_point = models.ForeignKey(PointsModel,
                                    on_delete=models.CASCADE,related_name='to_point'
                                    )

    # get point line ids as tuple

    def get_from_city(self):
        return self.from_point.city
    
    def get_to_city(self):
        return self.to_point.city

    def __str__(self):
        return f'{self.from_point.city} - {self.to_point.city}'
