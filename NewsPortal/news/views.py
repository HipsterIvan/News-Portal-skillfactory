from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.views import View
from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Post
from datetime import datetime
from .filters import  PostFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView

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
    
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)
    
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type = 'NW')
    
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type = 'NW')
    
class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)
    
class ArticleUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type = 'AR')
    
class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news')
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type = 'AR')
    
@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.object.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news')


class CategoryListView(PostsList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-created_at')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_cotext_data(**kwargs)
        context['not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
    
    
@login_required
def subscribe(request, pk):
    uesr = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    
    message = 'Вы успешно подписались на рассылку новостей по следующей категории'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
        

    