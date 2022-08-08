import inspect

from django.contrib.auth.decorators import login_required
from django.http import (
    JsonResponse, HttpRequest,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseNotModified,
)
from django.shortcuts import render, HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateResponseMixin

from common.analize.analizetools import (
    p_dir, p_mro, p_glob, p_loc, p_type,
    delimiter, p_content, show_builtins,
    show_doc, console, console_compose, console_compose2
)


def analyze_view(request):
    # # --- console ---
    # p_type(request)
    # console(request.META)
    # delimiter()
    # console(request.GET)
    # delimiter()
    # console(request.GET.urlencode())
    # p_dir(request.POST)
    # delimiter()
    # p_type(request.GET)
    # p_dir(request.GET)
    # p_mro(request.GET)
    # console(request.headers)
    # delimiter()
    # print(request.META.get('HTTP_USER_AGENT'))
    # delimiter()
    # print(request.META.get('HTTP_X_REAL_IP'))
    # delimiter()
    # print(request.META.get('REMOTE_ADDR'))
    # delimiter()
    # print(inspect.isclass(request))
    # print(inspect.ismodule(request))
    # print(inspect.ismethod(request))
    # print(inspect.istraceback(request))
    # print(inspect.iscode(request))
    # print(inspect.isabstract(request))
    # print(type(request).__name__)
    # print(inspect.getclasstree(request))
    # delimiter()
    p_type(request)
    # # --- console ---

    if request.method == 'POST':
        # # --- console ---
        # console(request.FILES)
        # p_type(request.FILES)
        # p_dir(request.FILES)
        # p_mro(request.FILES)
        # delimiter()
        # console(request.POST)
        # delimiter()
        # console(request.POST.urlencode())
        # delimiter()

        # # --- console ---
        return JsonResponse({'status': 'ok', })

    return render(
        request=request,
        template_name='notes/experiments.html',
        context={}
    )
