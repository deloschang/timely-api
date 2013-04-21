from django.contrib.gis.db import models

class Polygon(models.Model):
    name = models.CharField(max_length=16)
    poly = models.PolygonField()
    objects = models.GeoManager()
