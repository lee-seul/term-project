from django.conf.urls import url
from wiki import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),        
    url(r'document/(?P<pk>\d+)/$', views.DocumentDetailView.as_view(), name='document'),
]


