from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    message = models.TextField()

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.name} - {self.email}"
