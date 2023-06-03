from pathlib import Path
from typing import Generator, IO
from django.db.models import Count

from django.shortcuts import get_object_or_404

from file.models import *

menu = [{'title': "Видео", 'url_name': 'video_list'},
        {'title': "Вики", 'url_name': 'wiki_list'},

        {'title': "Тесты", 'url_name': 'testing_list'},
        {'title': "Задания", 'url_name': 'task_list'},

       # {'title': "Сообщения", 'url_name': 'chat'},
]

class DataMixin:
    paginate_by = 20

    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        # if not self.request.file.is_aithenticated:
        #     user_menu.pop(1)
        #     user_menu.pop(2)
        #     user_menu.pop(3)
        #     user_menu.pop(4)
        #     user_menu.pop(5)


        context['menu'] = user_menu
        cats = Category.objects.annotate(Count(context["menu_selected"]))
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context

def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


def open_file(request, video_pk: int) -> tuple:
    _video = get_object_or_404(VideoCourse, pk=video_pk)

    path = Path(_video.file.path)

    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    content_range = request.headers.get('range')

    if content_range is not None:
        content_ranges = content_range.strip().lower().split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        content_range = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, content_range
