from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = HTMLField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def vote_score(self):
        up = self.votes.filter(is_upvote=True).count()
        down = self.votes.filter(is_upvote=False).count()
        return up - down

    def approved_comments(self):
        return self.comments.filter(is_approved=True).order_by('-created_at')



class Comment(models.Model):
    topic = models.ForeignKey(Topic, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.user} on {self.topic}'


class Vote(models.Model):
    topic = models.ForeignKey(Topic, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = ('topic', 'user')
    

class News(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    link = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def vote_score(self):
        up = self.votes.filter(is_upvote=True).count()
        down = self.votes.filter(is_upvote=False).count()
        return up - down

    def approved_comments(self):
        return self.comments.filter(is_approved=True).order_by('-created_at')


class NewsComment(models.Model):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.user} on {self.news}'


class NewsVote(models.Model):
    news = models.ForeignKey(News, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = ('news', 'user')

    def __str__(self):
        return f"{'Upvote' if self.is_upvote else 'Downvote'} by {self.user} on {self.news}"
