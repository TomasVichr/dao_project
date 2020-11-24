from django.db import models

class PageInfoModel(models.Model):
    parsed_url = models.URLField()
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=3000) #rare long decriptions do exist
    site_name = models.CharField(max_length=250)
    image_url = models.CharField(max_length=250)
    date = models.DateField()
