from django.urls import path
from store.views.dashboard import DashboardView

app_name = 'store'
urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
]