from django.db import models

class UrineImage(models.Model):
    image= models.ImageField(upload_to='urine_stick_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded at {self.uploaded_at}"

