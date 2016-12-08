from django.shortcuts import render
from wiki.models import *
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class IndexView(ListView):
    template_name = "wiki/index.html"
    model = Document

class DocumentDetailView(DetailView):
    model = Document

