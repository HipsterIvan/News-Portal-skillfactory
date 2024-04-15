from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostSearch.as_view()),
    path('create/', PostCreate.as_view()),
    path('<int:pk>/edit/', PostUpdate.as_view()),
    path('<int:pk>/delete/', PostDelete.as_view()),
    path('articles/create/', ArticleCreate.as_view()),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view()),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view()),
]
