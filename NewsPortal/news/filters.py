from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from .models import Post

class  PostFilter(FilterSet):
    class Meta:
        model = Post
        fields= [
            'title',
            'author',
            'date_in',
        ]
    
