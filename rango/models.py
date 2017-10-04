from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField(max_length=200)
    views = models.IntegerField(default=0)
    content = models.TextField()
    # pub_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# class Article(models.Model):
#     category = models.ForeignKey(Category)
#     title = models.CharField('标题', max_length=200, unique=True)
#     body = models.TextField('正文')
#     created_time = models.DateTimeField('创建时间', auto_now_add=True)
#
#     def __str__(self):
#         return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


# class Comment(models.Model):

