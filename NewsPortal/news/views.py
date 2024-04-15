from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from datetime import datetime
from .filters import  PostFilter
from django.urls import reverse_lazy
from .forms import PostForm

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
    ordering = '-date_in'
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'
    
class PostSearch(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'posts_search.html'
    context_object_name = 'post_search'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    
class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)
    
class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type = 'NW')
    
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type = 'NW')
    
class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)
    
class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type = 'AR')
    
class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news')
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type = 'AR')
    