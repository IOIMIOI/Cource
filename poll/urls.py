from django.urls import path

from .views import *


urlpatterns = [
    path("", ListTesting.as_view(), name="testing_list"),
    path('category/<slug:cat_slug>/', TestingCategory.as_view(), name='testing_category'),
    path("<slug:testing_slug>/", ShowPoll.as_view(), name="poll_list"),
]