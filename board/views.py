from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import resolve_url, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from .models import Category, CategorySubscriber, Announcement, Response
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404
from django.core.cache import cache
from .filters import AnnouncementFilter
from .forms import AnnouncementForm, ResponseForm


class HomePage(TemplateView):
    template_name = 'homepage.html'


class AnnouncementList(ListView):
    model = Announcement
    ordering = '-date_created'
    template_name = 'board/announcement_list.html'
    context_object_name = 'announcement_list'
    queryset = Announcement.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category')

        context['category'] = None
        context['already_subscribed'] = False

        if category_id:
            user = self.request.user
            category = cache.get_or_set(f'category-{category_id}', Category.objects.get(id=category_id))

            context['category'] = category
            if user.is_authenticated:
                context['already_subscribed'] = CategorySubscriber.objects.filter(category=category, user=user).exists()

        context['filter'] = self.filter
        return context

    def get_queryset(self):
        category_id = self.kwargs.get('category')
        if category_id:
            queryset = Announcement.objects.filter(category=category_id)
        else:
            queryset = super().get_queryset()

        self.filter = AnnouncementFilter(self.request.GET, queryset)
        return self.filter.qs


class AnnouncementCategorySubscribe(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        category = cache.get_or_set(
            f'category-{self.kwargs.get("category")}',
            Category.objects.get(id=self.kwargs.get('category'))
        )

        if not category or not user.is_authenticated:
            raise Http404

        category_subscriber = CategorySubscriber.objects.filter(category=category.id, user=user.id).first()

        if not category_subscriber:
            subscriber = CategorySubscriber.objects.create(category=category, user=user)
            subscriber.save()

            messages.success(request, "Congratulations, you are now subscribed to announcements in this category.")
        else:
            messages.error(request, "You are already subscribed to announcements in this category.")

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return resolve_url('announcement_category', category=kwargs.get('category'))


class AnnouncementCategoryUnsubscribe(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        category = cache.get_or_set(
            f'category-{self.kwargs.get("category")}',
            Category.objects.get(id=self.kwargs.get('category'))
        )

        if not category:
            raise Http404

        category_subscriber = CategorySubscriber.objects.filter(category=category.id, user=user.id).first()

        if category_subscriber:
            category_subscriber.delete()

            messages.success(request, "Congratulations, you are now unsubscribed to announcements in this category.")
        else:
            messages.error(request, "You are not subscribed to announcements in this category.")

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return resolve_url('announcement_category', category=kwargs.get('category'))


class AnnouncementSearch(ListView):
    model = Announcement
    template_name = 'board/announcement_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = AnnouncementFilter(self.request.GET, queryset)
        return self.filter.qs


class AnnouncementDetail(PermissionRequiredMixin, DetailView):
    model = Announcement
    template_name = 'board/announcement.html'
    context_object_name = 'announcement'
    permission_required = 'board.view_announcement'

    def get_object(self, *args, **kwargs):
        return cache.get_or_set(f'announcement-{self.kwargs["pk"]}', super().get_object(queryset=self.queryset))


class AnnouncementCreate(PermissionRequiredMixin, CreateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'board/announcement_edit.html'
    permission_required = 'board.add_announcement'

    def form_valid(self, form):
        author = self.request.user
        announcement = form.save(commit=False)
        announcement.author = author
        return super().form_valid(form)


class AnnouncementUpdate(PermissionRequiredMixin, UpdateView):
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'board/announcement_edit.html'
    permission_required = 'announcement.change_announcement'


class AnnouncementDelete(DeleteView):
    model = Announcement
    template_name = 'board/announcement_delete.html'
    success_url = reverse_lazy('announcement_list')
    permission_required = 'board.delete_announcement'


class ResponseList(ListView):
    model = Response
    ordering = '-date_created'
    template_name = 'board/response_list.html'
    context_object_name = 'response_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        announcement = self.kwargs.get('announcement')

        context['announcement'] = None

        if announcement:
            user = self.request.user
            context['announcement'] = cache.get_or_set(f'announcement-{announcement}', Announcement.objects.get(id=announcement))

        return context

    def get_queryset(self):
        announcement = self.kwargs.get('announcement')

        if announcement:
            queryset = Response.objects.filter(announcement=announcement)
        else:
            queryset = Response.objects.filter()

        return queryset


class ResponseCreate(PermissionRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'board/response_edit.html'
    permission_required = 'board.add_response'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.user = User.objects.get(username=self.request.user)
        response.announcement = Announcement.objects.get(pk=self.kwargs.get('announcement'))
        print(response)
        return super().form_valid(form)


class ResponseDetail(PermissionRequiredMixin, DetailView):
    model = Response
    template_name = 'board/response.html'
    context_object_name = 'response'
    permission_required = 'board.view_response'

    def get_object(self, *args, **kwargs):
        return cache.get_or_set(f'response-{self.kwargs["pk"]}', super().get_object(queryset=self.queryset))


class ResponseApprove(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        response = Response.objects.get(pk=kwargs.get('pk'))
        print(response)
        if not response.approved:
            response.approved = True
            response.save()

            messages.success(request, "Congratulations, response is now approved.")
        else:
            messages.error(request, "You are already approved this response.")

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return resolve_url('response_detail', pk=kwargs.get('pk'))


class ResponseDelete(DeleteView):
    model = Response
    template_name = 'board/response_delete.html'
    success_url = reverse_lazy('response_list')
    permission_required = 'board.delete_response'

