"""tilltheend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path
from forever import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.register, name='register'),
    path('', views.index, name='home'),
    path('todo', views.todoadd, name='todo'),
    path('translate', views.translate, name='translate'),
    path('texttospech', views.texttospech, name='texttospech'),
    path('qrcode', views.qrcode, name='qrcode'),
    path('weather', views.weather, name='weather'),
    path('download', views.download_video, name='download'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('doing/<int:id>', views.doing, name='doing'),
    path('finish/<int:id>', views.finish, name='finish'),
    path('history/<int:id>', views.history, name='history'),
    path('news', views.news, name='news'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)