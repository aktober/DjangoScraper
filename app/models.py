from django.db import models


class NewsModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    use_in_report = models.BooleanField(default=False)

    comments = models.IntegerField(null=True, blank=True)
    votes = models.IntegerField(null=True, blank=True)

    category = models.CharField(max_length=60)

    def __str__(self):
        return self.title
