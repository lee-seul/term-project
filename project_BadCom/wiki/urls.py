from django.conf.urls import url
from wiki import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),        
    url(r'^document/(?P<pk>\d+)/$', views.DocumentDetailView.as_view(), name='document'),
    url(r'^document/(?P<pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
    url(r'^document/new/$', views.document_new, name='document_new'),
    url(r'^document/(?P<pk>\d+)/edit/$', views.document_edit, name='document_edit'),
]


