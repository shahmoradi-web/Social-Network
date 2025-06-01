from django.core.mail import send_mail
from django.db.models.signals import m2m_changed,post_delete,post_save
from django.dispatch import receiver
from .models import Post,User

@receiver(m2m_changed, sender=Post.likes.through)
def user_likes_change(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


@receiver(post_delete, sender=Post)
def user_delete_post(sender, instance, **kwargs):
    author = instance.author
    subject = f'your post has been deleted'
    message = f'Your post has been deleted {author}'
    send_mail(subject, message, 'shahmoradinrges@gmail.com',
              [author.email], fail_silently=False)

# @receiver(post_save, sender=Post)
# def activity_post(sender, instance, **kwargs):
#     ActivityPost.objects.create(user=instance.author, post=instance)

@receiver(post_save, sender=User)
def default_value(sender, instance, **kwargs):

    if not instance.bio:
        instance.bio = 'I am using this app'
        instance.save()

    if not instance.first_name:
        instance.first_name = instance.username
        instance.save()

    if not instance.photo:
        instance.photo = 'download.jpg'
        instance.save()