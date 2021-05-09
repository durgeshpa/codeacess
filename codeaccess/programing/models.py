from django.db import models
from account.models import User
from PIL import Image
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from codeaccess.settings import BASE_DIR
import os
from django.utils import timezone


def profile_image(instance, filename):
    """Rename file .."""
    ext = filename.split('.')[-1]
    # return settings.BASE_DIR + '/media/profile_image' + instance.user.username + ext
    path = BASE_DIR + '/media/' + 'profile_image/' + str(instance.user.pk)
    if os.path.exists(path):
        try:
            temp = os.listdir(path=path)
            os.remove(path + '/' + temp[0])
        except:
            pass

    return 'profile_image/' + str(instance.user.pk) + "/" + str(instance.user.pk) + '.' + ext


class PublishedManager(models.Manager):
    """custmize object ..."""

    def get_queryset(self):
        """Query set in user manager.."""
        return super(PublishedManager, self).get_queryset().filter(status='published')


class CLanguage(models.Model):
    """clanguage problem .."""

    # user = models.ForeignKey(CLanguage, on_delete=set)
    # user = models.ManyToManyField(Profile, blank=True)

    choice = (
             ('draft', 'Draft'),
             ('published', 'Published'),)
    option = (('easy', 'Easy'),
              ('medium', "medium"),
              ('Hard', 'Hard'))
    # usr = models.ForeignKey(Profile, on_delete)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='c_posts',)
    lavel = models.CharField(max_length=10, choices=option, default='easy')
    problem = models.TextField()
    testcase = models.TextField()
    output = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=choice,
                              default='draft')

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom  manager.

    class Meta:
        """meta class of Post model.."""

        ordering = ('-publish',)

    def __str__(self):
        """Return object name in user readable.."""
        return self.title

    def get_absolute_url(self):
        """Canonical URLs for models.."""
        return reverse("programing:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Profile(models.Model):
    """user profile model .."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True, max_length=25)
    image = models.FileField(upload_to=profile_image, default='profile_image/default.jpeg')
    collegename = models.CharField(blank=True, max_length=225)
    about = models.TextField(blank=True, null=True)
    roll_no = models.CharField(blank=True, max_length=10)
    course = models.CharField(blank=True, max_length=25)
    branch = models.CharField(blank=True, max_length=25)
    # status = models.CharField(max_length=250)

    class Meta:
        """meta class.."""

        managed = True

    def __str__(self):
        """Return object name.."""
        return self.user.username

    def save(self, *args, **kwargs):
        """Save method .."""
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        # self.image.path = settings.BASE_DIR + 'media/profile_image' + str(self.user.username) + '.jpg'

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            print(self.image.path)
            super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Createing user profile .."""
    if created:
        Profile.objects.create(user=instance)
    if not instance.profile.name:
        instance.profile.name = instance.username

    instance.profile.save()


class ClanguageslveStatus(models.Model):
    """docstring for ClassName .."""

    pass
