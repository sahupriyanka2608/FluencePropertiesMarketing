import requests
import json
from dataextractor.models import Post,Comment, User
from dataextractor.api.serializers import PostSerializer, CommentSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
class ScheduleJob:
    def fetch_comments_from_facebook(post_id):
        params = {
       'access_token': 'EAAKrDSaXrgABO4AqNjolRBUtIJdcoPXwjHNQaVD0rgZCFNGejoi6w5hV3CE0nkqGS3qLfMkZAw3So45hZBrkgahyMcipFLvHy2kO6iKPqzbSfE8wO29r7ZAKmJ4VdQFTxZBtGjCStlzkSDxz8r6YvQ6rD3ZAQDuzBZCZB0RLOHMAnxpYKEockG1uvjkAKiYU8Kk6',
        }
        endpoint = 'https://graph.facebook.com/v19.0/#post_id/comments'

        response = requests.get(endpoint.replace('#post_id',post_id), params=params)
        return json.loads(response.content)['data']
    def my_scheduled_job():
        params = {
        'fields': 'message,created_time,attachments,admin_creator',
        'access_token': 'EAAKrDSaXrgABO4AqNjolRBUtIJdcoPXwjHNQaVD0rgZCFNGejoi6w5hV3CE0nkqGS3qLfMkZAw3So45hZBrkgahyMcipFLvHy2kO6iKPqzbSfE8wO29r7ZAKmJ4VdQFTxZBtGjCStlzkSDxz8r6YvQ6rD3ZAQDuzBZCZB0RLOHMAnxpYKEockG1uvjkAKiYU8Kk6'}

        response = requests.get('https://graph.facebook.com/v19.0/288268867694838/posts', params=params)
        data = json.loads(response.content)['data']
        for input in data:
            post_id=input['id']
            try:
                post=Post.objects.get(post_id=post_id)
                serializer=PostSerializer(post,data=input)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors)        
            except:
                serializer=PostSerializer(data=input)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors)
            ScheduleJob.get_comments_for_post(post_id)
                
         
    def get_comments_for_post(postid):
        data = ScheduleJob.fetch_comments_from_facebook(postid)
        for input in data:
            input = ScheduleJob.map_fb_model_to_comment(input, postid)
            print(input)
            comment_id = input['comment_id']
            try:
                comment=Comment.objects.get(comment_id=comment_id)
                serializer=CommentSerializer(comment,data=input)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors)        
            except:
                user_serializer = UserSerializer(data=input)
                if user_serializer.is_valid():
                    user_serializer.save()
                # user = User.objects.get(user_id=input['user_id'])
                # post = Post.objects.get(post_id=input['post_id'])
                # input['user_id'] = user
                # input['post_id'] = post
                serializer=CommentSerializer(data=input)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors)
    
    def map_fb_model_to_comment(input, post_id):
        comment = {}
        comment['user_id'] = input['from']['id']
        comment['username'] = input['from']['name']
        comment['post_id'] = post_id
        comment['comment_id'] = input['id']
        comment['created_time'] = input['created_time']
        comment['message'] = input['message']
        return comment
             
                       
                
            
                
    