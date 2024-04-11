from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime
from .filters import  PostFilter
from django.urls import reverse_lazy

class PostsList(ListView):
    model = Post
    ordering = 'date_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
    
    
    
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    
class PostSearch(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'posts_search.html'
    context_object_name = 'post_search'
    paginate_by = 3
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context