from django.urls import path
from . import views
from . import api_views
from django.shortcuts import render
app_name = 'blog'

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('topic/new/', views.topic_create, name='topic_create'),
    path('topic/<slug:slug>/', views.topic_detail, name='topic_detail'),
    path('topic/<slug:slug>/edit/', views.edit_topic, name='topic_edit'),
    path('topic/<slug:slug>/delete/', views.delete_topic, name='topic_delete'),
    path('topic/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('topic/<slug:slug>/vote/<str:vote_type>/', views.topic_vote, name='topic_vote'),
    
    path('api/topics/', api_views.TopicListAPI.as_view(), name='api_topic_list'),
    path('api/topics/<slug:slug>/', api_views.TopicDetailAPI.as_view(), name='api_topic_detail'),
    path('api/topics/<slug:slug>/comments/', api_views.CommentListAPI.as_view(), name='api_topic_comments'),

    path('test', views.test_view, name='test'),
    path('news', views.news, name='news'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/thanks/', lambda request: render(request, 'contact_thanks.html'), name='contact_thanks'),
    path('about/', views.about_view, name='about'),
    path('topics', views.all_topics_view, name='all_topics'),
    path('wifi_coverage', views.wifi_coverage, name='wifi_coverage'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
