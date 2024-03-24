"""levicommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path
from Levi import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home,name='home'),
    path('test/',views.test,name='test'),
    path('signin/',views.signin,name='signin'),
    path('category/',views.category_view,name='category'),
    path('pdlist/<int:category_id>/',views.product_list,name="pdlist"),
    path('signout/',views.signout,name="signout"),
    path('buynow/<int:product_id>/',views.buy_now,name="buy_now"),
    path('signup/',views.register,name="signup"),
    path('complete_profile/',views.complete_profile, name='complete_profile'),
    path('edit_profile/',views.edit_profile, name='edit_profile'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm_checkout/', views.confirm_checkout, name='confirm_checkout'),
    re_path(r'^.*/$', views.custom_404_view),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
