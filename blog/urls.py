from django.urls import path
from . views import *
urlpatterns = [
    path('home/',HomeView,name='home'),
    # path('home/',PostListView,name='postList'),
    path('tag/<slug:slug>/',tagged,name='tagged'),
    path('search/',searchView,name='searchView'),
    path('AddComment/',AddComment,name='AddComment'),
    path('post-Create/',PostCreate,name='PostCreate'),
    path('post-category/',CategoryCreate,name='CategoryCreate'),
    path('post/',PostListView,name='postList'),
    path('post-details/<int:id>/',PostDetails,name='PostDetails'),
    path('post-Edit/<int:id>/',PostEdit,name='PostEdit'),
    path('post-Delete/<int:id>/',PostDelete,name='PostDelete'),
]