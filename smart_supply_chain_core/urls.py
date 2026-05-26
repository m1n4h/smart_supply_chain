from django.contrib import admin
from django.urls import path
from forecasting import views  #  Correctly target your forecasting folder!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dynamic_dashboard_view, name='dashboard'), # Root landing page
]