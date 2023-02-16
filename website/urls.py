from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
	path('',TemplateView.as_view(template_name='web/index.html'), name='index'),
	re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]