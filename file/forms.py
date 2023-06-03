from django import forms

from .models import *


class AddTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task'].empty_label = "Задание не выбрано"


    class Meta:
        model = TaskAnswer
        fields = ['task', 'file']

    #
    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) > 200:
    #         raise ValidationError('Длина превышает 200 символов')
    #
    #     return title

