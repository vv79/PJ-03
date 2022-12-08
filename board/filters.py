from django_filters import FilterSet, CharFilter, DateTimeFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import Post, Category
from django.utils.translation import gettext_lazy as _


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        label=_('Title'),
        lookup_expr='icontains'
    )
    category = ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label=_('Category'),
        empty_label='Choose category ...'
    )
    added_after = DateTimeFilter(
        field_name='date_created',
        label=_('Added after'),
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}
        ),
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'added_after']

    def is_applied(self):
        return self.form.is_valid() and any(self.form.cleaned_data.values())
