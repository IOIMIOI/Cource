from django.urls import path

from file.views import *

urlpatterns = [
    path('', home, name='home'),

    path('video/', ListVideo.as_view(), name='video_list'),
    path('video/category/<slug:cat_slug>/', VideoCategory.as_view(), name='video_category'),
    path('video/<slug:video_slug>/', ShowVideo.as_view(), name='video'),
    path('video/stream/<int:pk>/', get_streaming_video, name='stream'),

    path('wiki/', ListWiki.as_view(), name='wiki_list'),
    path('wiki/category/<slug:cat_slug>/', WikiCategory.as_view(), name='wiki_category'),
    # path('wiki/<slug:wiki_slug>/', ShowWiki.as_view(), name='wiki'),

    path('task/', ListTask.as_view(), name='task_list'),
    path('task/category/<slug:cat_slug>/', TaskCategory.as_view(), name='task_category'),
    path('task/<slug:task_slug>/', ShowTask.as_view(), name='task'),
    #path('task/answer', LoadTask.as_view(), name='task_answer'),
    path('task/answer', LoadTask, name='task_answer'),

]