from django.conf.urls import include, url
from hello import views as list_views
from hello import urls as list_urls

urlpatterns = [
    url(r'^$', list_views.index, name='index'),
    url(r'^lists/', include(list_urls)),
    # url(r'^admin/', include(admin.site.urls)),
]
