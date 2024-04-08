from dataextractor.models import Post,Comment,User
from dataextractor.api.serializers import PostSerializer,CommentSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from dataextractor.api.cron import ScheduleJob

class Dataextraction(APIView):
    def get(self, request):
        ScheduleJob.my_scheduled_job()
        content = {'Status': 'Infromation stored in DB successfully'}
        return Response(content)
    
class PostListAV(APIView):
    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True) 
        return Response(serializer.data)
class CommentListAV(APIView):
    def get(self,request,postid):
        comments = Comment.objects.all()
        try:
            post = Post.objects.get(post_id = postid)
        except Post.DoesNotExist:        #if particular id is not found
            return Response({'Error': 'Post not found'})
        comments = Comment.objects.filter(post_id=postid)
        serializer = CommentSerializer(comments,many=True) 
        return Response(serializer.data)  
class UserListAV(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True) 
        return Response(serializer.data)    
    