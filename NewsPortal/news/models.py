from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 0)
    def update_rating(self):
        postR = self.post_set.all().aggregate(postRating = Sum('rating'))
        p_R = 0
        p_R += postR.get('postRating')
        
        commentR = self.authorUser.comment_set.aggregate(commenrRating = Sum('rating'))
        c_R = 0
        c_R += commentR.get('commenrRating')
        
        self.ratingAuthor = p_R * 3 + c_R
        self.save
    
class Category(models.Model):
    name = models.CharField(max_length = 26, unique = True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')
    
    def __str__(self):
        return self.name.title()
    
class Post(models.Model):
    news = "NW"
    articles = "AR"
    POST_TYPES = [
        (news, "Новости"),
        (articles, "Статья")
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length = 2, choices = POST_TYPES, default = news)
    date_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length = 128)
    text = models.TextField()
    rating = models.IntegerField(default = 0)
    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()
    def preview(self):
        return self.text[:124] + '...'
    def get_absolute_url(self):
        return f'/news/{self.id}'
    
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    date_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default = 0)
    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()