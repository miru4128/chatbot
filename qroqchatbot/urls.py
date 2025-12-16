from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # ✅ Redirect root URL to cattle-chat
    path("", RedirectView.as_view(url="/cattle-chat/", permanent=False)),

    path("cattle-chat/", include("cattle_chat.urls")),
    path("admin/", admin.site.urls),
]
