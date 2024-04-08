from django.urls import path,include
from dataextractor.api.views import PostListAV,Dataextraction,CommentListAV,UserListAV
from dataextractor.api import views

urlpatterns = [
    path("list/",PostListAV.as_view(),name='postlist'),
    path("extract/",Dataextraction.as_view(),name='postdetails'),
    path("comment/<str:postid>",CommentListAV.as_view(),name='commentlist'),
    path("user/",UserListAV.as_view(),name='userlist'),
]