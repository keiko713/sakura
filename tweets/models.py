from django.db import models

class GeoData(models.Model):
    geo_address = models.CharField(max_length=100)
    geo_lat = models.CharField(max_length=20)
    get_lng = models.CharField(max_length=20)


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=30)
    urlize_text = models.CharField(max_length=1000)
    tco_url = models.CharField(max_length=200)
    photo_siteurl = models.CharField(max_length=200)
    photo_imgsrc = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    geo_location = models.CharField(max_length=100)
    geo_date = models.ForeignKey(GeoData)
    username = models.CharField(max_length=20)


class BlackList(models.Model):
    tco_url = models.CharField(max_length=200, null=True)
    screen_name = models.CharField(max_length=20, null=True)
