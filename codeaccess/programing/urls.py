from django.conf.urls import url
from django.urls import path
from . import views
app_name = 'programing'
urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'edit$', views.updateprofile, name='updateprofile'),
    url('edidprofileimg', views.updatepofileimg, name='updateimage'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,
         name='post_detail'),

    url(r'list/clanguge', views.CList.as_view(), name="clist"),
    url(r'execute$', views.execute, name='execute')
]
