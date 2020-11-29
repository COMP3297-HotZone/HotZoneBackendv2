"""hotzone_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from addLocation.views import *
from viewCases.views import *
from cluster.views import *
from login.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('logout/', logout_view),
    path('', auth_views.LoginView.as_view(template_name='login.html')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('create_caserecord_post/', CaseRecordAPI.as_view(),
         name='create_caserecord_post'),
    path('create_visitedlocation_post/', CreateVisitedLocationAPI.as_view(),
         name='create_visitedlocation_post'),
    path('create_caserecord/', CreateCaseRecordView.as_view(),
         name="create_caserecord"),
    path('post_caserecord/', CreateCaseRecordAPI.as_view(), name="post_caserecord"),
    path('create_virus/', CreateVirusView.as_view(), name='create_virus'),
    path('post_create_virus/', CreateVirusAPI.as_view(), name='post_create_virus'),
    path('index/', IndexView.as_view(), name='index'),
    path('create_visitedlocation/<int:caseID>',
         CreateVisitedLocationView.as_view(), name='create_visitedlocation'),
    path('locations/', LocationView.as_view(), name='locations-information'),
    path('search_location_post/', LocationWithMatchOnTopView.as_view(),
         name='search_location_post'),
    path('all_caserecord_post/<int:pk>/', ViewLocationRecordsView.as_view(),
         name="viewLocationRecords"),
    path('all_caserecord_post/', AllCaseRecord.as_view(),
         name="all_caserecord_post"),
    path('search_caserecord_post/', SearchCaseRecord.as_view(),
         name='search_caserecord_post/'),
     path('all_caserecord_get/', AllCaseRecordAPI.as_view(), name='all_caserecord_get'),
     path('cluster_get/', ClusterAPIView.as_view(), name='cluster_get'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
