import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django_resized import ResizedImageField
from taggit.managers import TaggableManager

# Create your models here.

class User(AbstractUser):
    data_of_brith = models.DateField(verbose_name='تاریخ تولد', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, verbose_name='بیوگرافی')
    photo = models.ImageField(upload_to='account_images/',
                              verbose_name='تصویر', default='download.jpg')
    job = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False,through='Cancat')




class Post(models.Model):
    image = models.ManyToManyField('Image', blank=True, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts'
                               , verbose_name='نویسنده')

    description = models.TextField(verbose_name='توضیحات')
    active = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    saved_by = models.ManyToManyField(User, blank=True, related_name='saved_posts')
    total_likes = models.PositiveIntegerField(default=0)
    tags = TaggableManager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes'])
        ]


    def get_absolute_url(self):
        return reverse('social:post_detail', args=[self.id])


    def __str__(self):
        return self.author.first_name

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    imag_file = ResizedImageField(upload_to='post_images/', size=[500, 500], crop=['top', 'left'], quality=75)

    def delete(self, *args, **kwargs):
        storage, path = self.imag_file.storage, self.imag_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else os.path.basename(self.imag_file.url)


class Cancat(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_from_set')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
    def __str__(self):
            return f'{self.user_from} -> {self.user_to}'


