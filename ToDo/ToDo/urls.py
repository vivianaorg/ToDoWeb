from django.contrib import admin
from django.urls import include, path
from ToDoApp import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView,  TokenObtainPairView
from profiles import views as views_profile

router = routers.DefaultRouter()
#router.register(r"users", views.UserViewSet)
router.register(r"categorys", views.CategoryViewSet)
router.register(r"task", views.TaskViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("ToDoApp/", include("ToDoApp.urls")),
    path('token/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('api-token-auth/', obtain_auth_token),
    #path('api-token-auth/', views.CustomAuthToken.as_view()),
    path("tokenjwt/",TokenObtainPairView.as_view(), name="token_obtain_pair"), 
    path("tokenjwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path("users-create/", views_profile.ProfileCreationView.as_view(), name="profile-create"),
    path("users-list/", views_profile.ProfileDetailView.as_view(), name="profile-detail"),
]
