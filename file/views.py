from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from .utils import *

class ListVideo(DataMixin, ListView):
    model = VideoCourse
    template_name = 'file/video_list.html'
    context_object_name = 'video_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Все видео",menu_selected="videocourse")
        return dict(list(context.items())+list(c_def.items()))

class ShowVideo(DataMixin, DetailView):
    model = VideoCourse
    template_name = "file/video.html"
    slug_url_kwarg = "video_slug"
    context_object_name = "video"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Видео",menu_selected="videocourse")
        return dict(list(context.items())+list(c_def.items()))

class VideoCategory(DataMixin, ListView):
    model = VideoCourse
    template_name = 'file/video_list.html'
    context_object_name = 'video_list'
    allow_empty = False

    def get_queryset(self):
        return VideoCourse.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk,menu_selected="videocourse")
        return dict(list(context.items()) + list(c_def.items()))

def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response

##########################################################

class ListWiki(DataMixin, ListView):
    model = Wiki
    template_name = 'file/wiki_list.html'
    context_object_name = 'wiki_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вики", menu_selected="wiki")
        return dict(list(context.items())+list(c_def.items()))

# class ShowWiki(DataMixin, DetailView):
#     model = Wiki
#     template_name = "file/wiki.html"
#     slug_url_kwarg = "wiki_slug"
#     context_object_name = "wiki"
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Wiki", menu_selected="wiki")
#         return dict(list(context.items())+list(c_def.items()))

class WikiCategory(DataMixin, ListView):
    model = Wiki
    template_name = 'file/wiki_list.html'
    context_object_name = 'wiki_list'
    allow_empty = False

    def get_queryset(self):
        return Wiki.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk, menu_selected="wiki")
        return dict(list(context.items()) + list(c_def.items()))

##########################################################

class ListTask(DataMixin, ListView):
    model = Tasks
    template_name = 'file/task_list.html'
    context_object_name = 'task_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Задания", menu_selected="tasks")
        return dict(list(context.items())+list(c_def.items()))

class ShowTask(DataMixin, DetailView):
    model = Tasks
    template_name = "file/task.html"
    slug_url_kwarg = "task_slug"
    context_object_name = "task"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Задания", menu_selected="tasks")
        return dict(list(context.items())+list(c_def.items()))

# class LoadTask(LoginRequiredMixin, DataMixin, CreateView):
#     form_class = AddTaskForm
#     template_name = 'file/task_answer.html'
#     success_url = reverse_lazy('home')
#     login_url = reverse_lazy('home')
#     raise_exception = True
#
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Добавление ответа", menu_selected="tasks")
#         return dict(list(context.items()) + list(c_def.items()))

def LoadTask(request):
    data = request.POST.copy()
    data.update({'user': request.user})
    form = AddTaskForm(data)

    if form.is_valid():
        form.user = request.user
        form.save()
        return redirect('home')
    else:
        form = AddTaskForm()

    return render(request, 'file/task_answer.html', {'form': form})



class TaskCategory(DataMixin, ListView):
    model = Tasks
    template_name = 'file/task_list.html'
    context_object_name = 'task_list'
    allow_empty = False

    def get_queryset(self):
        return Tasks.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk, menu_selected="tasks")
        return dict(list(context.items()) + list(c_def.items()))

##########################################################

def view_invoice(request, wiki_slug):
    wiki = get_object_or_404(Wiki, slug=wiki_slug)
    context = {
        'wiki': wiki,

    }

    return render(request, 'wiki.html', context=context)

def home(request):
    context = {
        'menu': menu,
        'title': "Main"
    }
    return render(request, 'file/home.html', context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
