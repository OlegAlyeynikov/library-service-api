from django.db import models


class Book(models.Model):
    COVER_CHOICES = [("HARD", "Hard cover"), ("SOFT", "Soft cover")]
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=256)
    cover = models.CharField(max_length=15, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return (
            f"'{self.title}' by {self.authors}, "
            f"cover: {self.cover}, "
            f"daily fee: {self.daily_fee}, "
            f"inventory: {self.inventory}"
        )
