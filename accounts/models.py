from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
def upload_image_rename(instance, filename):
    filebase, extenstion = filename.split(".")
    return "images/userprofile/%s.%s" % (instance.user.username, extenstion)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    karma = models.IntegerField(default=0)
    about = models.CharField(max_length=250, blank=True)
    image = models.ImageField(
        upload_to="images/userprofile/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.username

    def save(self):
        super().save()  # saving image first
        img = Image.open(self.image.path)  # Open image using self
        if img.height > 250 or img.width > 250:
            new_img = (250, 250)
            img.thumbnail(new_img)
            img.save(self.image.path)  # saving image at the same path
