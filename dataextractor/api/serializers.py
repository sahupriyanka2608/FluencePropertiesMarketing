from rest_framework import serializers
from dataextractor.models import Post,Comment,User
class PostSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(source='post_id')
    class Meta:
        model = Post
        fields = "__all__"
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"                