from django.shortcuts import render, redirect, get_object_or_404
from wiki.models import *
from django.views.generic import ListView, DetailView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from wiki.forms import *


class IndexView(ListView):
    template_name = "wiki/index.html"
    model = Document
    

class DocumentDetailView(DetailView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentNew
        return context

#class CommentCreateView(FormView):
#    form_class = CommentNew
#    template_name = "wiki/document_detail.html"
#
#    def form_valid(self, form):
#        return super(CommentCreateView, self).form_valid(form)

def comment_new(request, pk):
    if request.method == 'POST':
        form = CommentNew(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.document = Document.objects.get(pk=pk)
            comment.save()
            return redirect('wiki:document', pk)
    else:
        form = CommentNew()
    return render(request, 'document_detail.html', {
        'form': form,
        'pk' : pk,
        })

def document_new(request):
    #form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.save()
            return redirect('wiki:document', pk=document.pk)
    else:
        form = DocumentForm()
    return render(request, 'wiki/document_new.html', {'form': form})

def document_edit(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            document = form.save(commit=False)
            document.save()
            return redirect('wiki:document', pk=document.pk)
    else:
        form = DocumentForm(instance=document)
    return render(request, 'wiki/document_edit.html', {'form':form})


