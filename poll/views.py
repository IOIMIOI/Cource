from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from .models import *

from file.utils import DataMixin

class ListTesting(DataMixin, ListView):
    model = Testing
    template_name = 'poll/testing_list.html'
    context_object_name = 'testing_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Все Тесты", menu_selected="testing")
        return dict(list(context.items())+list(c_def.items()))
#
# class ShowPoll(DataMixin, ListView):
#     model = Poll
#     template_name = "poll/poll_list.html"
#     slug_url_kwarg = "poll_slug"
#     context_object_name = "poll_list"
#
#     def get_queryset(self):
#         return Poll.objects.filter(testing__slug=self.kwargs['testing_slug']).select_related('testing')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Тест", menu_selected="poll")
#         return dict(list(context.items())+list(c_def.items()))
#
class ShowPoll(DataMixin, DetailView):
    model = Testing
    template_name = "poll/poll.html"
    slug_url_kwarg = "testing_slug"
    context_object_name = "testing"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Задания", menu_selected="testing")
        return dict(list(context.items())+list(c_def.items()))

class TestingCategory(DataMixin, ListView):
    model = Testing
    template_name = 'poll/testing_list.html'
    context_object_name = 'testing_list'
    allow_empty = False

    def get_queryset(self):
        return Testing.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk, menu_selected="testing")
        return dict(list(context.items()) + list(c_def.items()))

class HomeView(View):

    def get(self, request):
        polls = Poll.objects.all()
        return render(
            request,
            template_name="poll/home.html",
            context={
                "polls": polls,
            }
        )

class PollView(View):

    def get(self, request, poll_id):
        poll = Poll.objects.get(id=poll_id)
        return render(
            request,
            template_name="poll/poll.html",
            context={
                "poll": poll,
            }
        )

    def post(self, request, poll_id):
        requestData = request.POST

        choice_id = requestData.get('choice_id')

        poll = Poll.objects.get(id=poll_id)
        choice = Choice.objects.get(id=choice_id)
        Vote.objects.create(
            poll=poll,
            choice=choice,
        )

        poll_results = []
        for choice in poll.choices.all():
            voteCount = Vote.objects.filter(poll=poll, choice=choice).count()
            poll_results.append([choice.name, voteCount])

        return render(
            request,
            template_name="poll/poll.html",
            context={
                "poll": poll,
                "success_message": "Voted Successfully",
                "poll_results": poll_results,
            }
        )