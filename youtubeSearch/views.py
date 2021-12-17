import os

from django.http import FileResponse, Http404
from django.shortcuts import render
from django.utils.encoding import escape_uri_path


def index(request):
    return render(request, 'search.html')

def download(request, file_path):
    try:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename={}'.format(escape_uri_path(os.path.basename(file_path)))
        return response
    except Exception:
        raise Http404
