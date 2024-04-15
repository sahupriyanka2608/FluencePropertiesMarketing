import requests
import json
from dataextractor.models import Post,Comment, User
from dataextractor.api.serializers import PostSerializer, CommentSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
class ScheduleJob:
    fb_access_token = ''
    ig_access_token = 'EAAN1MbEKJPQBOyAYsMlGJDN33GF0ZBK8WpnkeEIEgGEeZBKAunBFhZCyJbH0ITc7ZCZCLuzZBnUZCJgmUXkTxFRbvvLHEmCUNAhevZCPjmEnrm9IKMWVSdy7hk7cAT60C9pU9hqzuV6ZANLfQln5XvlW5vPFTJLHd91zB3po5KLSVDwpheBIYBUEsY8nI'
    
    def fetch_post_from_instagram():
        params = {
        'fields': 'caption,id,ig_id,media_type,media_url,timestamp',
        'access_token': ScheduleJob.ig_access_token
        }

        response = requests.get('https://graph.facebook.com/v19.0/17841448496234200/media', params=params)
        print(response.content)
        return json.loads(response.content)['data']
    
    def fetch_post_from_fb():
        params = {
        'fields': 'message,created_time,attachments,admin_creator',
        'access_token': ScheduleJob.fb_access_token
        }

        response = requests.get('https://graph.facebook.com/v19.0/288268867694838/posts', params=params)
        return json.loads(response.content)['data']
    
    def fetch_comments_from_instagram(ig_media_id):
        params = {
        'fields': 'id,from,text,timestamp',
        'access_token': ScheduleJob.ig_access_token
        }
        endpoint = 'https://graph.facebook.com/v19.0/#post_id/comments'
        response = requests.get(endpoint.replace('#post_id',ig_media_id), params=params)
        return json.loads(response.content)['data']
        # response = requests.get('https://graph.facebook.com/v19.0/17912316830806375/comments', params=params)
        
    def fetch_comments_from_facebook(post_id):
        params = {
        'access_token': ScheduleJob.fb_access_token
        }
        endpoint = 'https://graph.facebook.com/v19.0/#post_id/comments'

        response = requests.get(endpoint.replace('#post_id',post_id), params=params)
        return json.loads(response.content)['data']
    
    def save_in_db(serializer):
        if serializer.is_valid():   
            serializer.save()
        else:
            print(serializer.errors)
            return Response(serializer.errors)
    
    def save_comment(input):
        comment_id = input['comment_id']
        try:
            comment=Comment.objects.get(comment_id=comment_id)
            serializer=CommentSerializer(comment,data=input)
            ScheduleJob.save_in_db(serializer)        
        except:
            user_serializer = UserSerializer(data=input)
            ScheduleJob.save_in_db(user_serializer)
            serializer=CommentSerializer(data=input)
            ScheduleJob.save_in_db(serializer)
            
    def save_post(input):
        post_id=input['post_id']
        try:
            post=Post.objects.get(post_id=post_id)
            serializer=PostSerializer(post,data=input)
            ScheduleJob.save_in_db(serializer)
        except:
            serializer=PostSerializer(data=input)
            ScheduleJob.save_in_db(serializer)    
    
    def my_scheduled_job():
        # ScheduleJob.save_fb_media_data()
        ScheduleJob.save_ig_media_data()
    
    def save_fb_media_data():
        data = ScheduleJob.fetch_post_from_fb()
        for input in data:
            input = ScheduleJob.map_fb_post_model_to_post(input)
            post_id = input['post_id']
            ScheduleJob.save_post(input)
            ScheduleJob.save_fb_comments_for_post(post_id)
        
         
    def save_fb_comments_for_post(postid):
        data = ScheduleJob.fetch_comments_from_facebook(postid)
        for input in data:
            input = ScheduleJob.map_fb_model_to_comment(input, postid)
            ScheduleJob.save_comment(input)
    
    def save_ig_media_data():
        data = ScheduleJob.fetch_post_from_instagram()
        for input in data:
            input = ScheduleJob.map_ig_post_model_to_post(input)
            post_id = input['post_id']
            ScheduleJob.save_post(input)     
            ScheduleJob.save_ig_comments_for_post(post_id)
        
         
    def save_ig_comments_for_post(postid):
        data = ScheduleJob.fetch_comments_from_instagram(postid)
        for input in data:
            input = ScheduleJob.map_ig_model_to_comment(input, postid)
            ScheduleJob.save_comment(input)
    
            
    def map_fb_model_to_comment(input, post_id):
        comment = {}
        comment['user_id'] = input['from']['id']
        comment['username'] = input['from']['name']
        comment['post_id'] = post_id
        comment['comment_id'] = input['id']
        comment['created_time'] = input['created_time']
        comment['message'] = input['message']
        comment['source'] = "FB"
        return comment
    
    def map_ig_model_to_comment(input, post_id):
        comment = {}
        comment['user_id'] = input['from']['id']
        comment['username'] = input['from']['username']
        comment['post_id'] = post_id
        comment['comment_id'] = input['id']
        comment['created_time'] = input['timestamp']
        comment['message'] = input['text']
        comment['source'] = "IG"
        return comment
    
    def map_ig_post_model_to_post(input):
        print(input)
        post = {}
        post['created_time'] = input['timestamp']
        post['post_id'] = input['id']
        if 'caption' in input:
            post['message'] = input['caption']
        else :
            post['message'] = "N/A"
        post['source'] = "IG"
        attachments = {}
        if 'media_type' in input:
            attachments['media_type'] = input['media_type']
        if 'media_url' in input:    
            attachments['media_url'] = input['media_url']
        post['attachments'] = attachments
        return post
    
    def map_fb_post_model_to_post(input):
        post = {}
        post['created_time'] = input['created_time']
        post['post_id'] = input['id']
        post['message'] = input['message']
        post['source'] = "FB"
        post['attachments'] = input['attachments']
        return post
             
                       
                
            
                
    