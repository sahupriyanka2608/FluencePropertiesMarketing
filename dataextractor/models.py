from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=200, primary_key=True)
    username = models.CharField(max_length=200)
class Post(models.Model):
    created_time = models.DateTimeField()
    post_id = models.CharField(max_length=200, primary_key=True)
    message = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True, default= "FB")
    attachments = models.JSONField(null=True, blank=True)
    
class Comment(models.Model):
    user_id = models.ForeignKey(User,to_field="user_id",on_delete=models.CASCADE,related_name="commentsbyuser")
    comment_id = models.CharField(max_length=200, primary_key=True)
    message = models.CharField(max_length=200, null=True)
    source = models.TextField(null=True, blank=True, default="FB")
    post_id = models.ForeignKey(Post,on_delete = models.CASCADE,related_name="comments")
    created_time = models.DateTimeField(null=True)
