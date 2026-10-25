
from django.contrib import admin
from django.urls import path, include
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage displays the product listing
    path('', views.product_list, name='home'),

    # Existing store URLs
    path('', include('store.urls')),
]
