from django.http import HttpRequest, HttpResponse ,JsonResponse
import os
from os.path import join


def delete_file(old_file=""):
    os.remove(os.path.join(settings.MEDIA_ROOT, old_file))


def ajax_response(uid=""):
    if uid:
        status = 1
    else:
        status = 0
    return HttpResponse(status)