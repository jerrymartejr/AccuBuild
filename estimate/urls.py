from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("create_new_project", views.create_new_project, name="create_new_project"),
    path("add_new_client", views.add_new_client, name="add_new_client"),
    path("summary/<int:project_id>", views.project, name="project"),
    path("detailed/<int:project_id>", views.detailed, name="detailed"),
    path("add_divisions/<int:project_id>", views.add_divisions, name="add_divisions"),
    path("remove_division/<int:project_id>", views.remove_division, name="remove_division"),
    path("add_scope/<int:project_id>", views.add_scope, name="add_scope"),
    path("add_new_divison/<int:project_id>", views.add_new_division, name="add_new_division"),
    path("remove_scope/<int:project_id>", views.remove_scope, name="remove_scope"),
    path("add_item/<int:project_id>", views.add_item, name="add_item"),
    path("remove_item/<int:project_id>", views.remove_item, name="remove_item"),
    path('get_scope_items/<int:scope_id>/', views.get_scope_items, name='get_scope_items'),
    path("update_markup/<int:project_id>", views.update_markup, name="update_markup"),
    path("submit_for_approval/<int:project_id>", views.submit_for_approval, name="submit_for_approval"),
    path("estimator_projects", views.estimator_projects, name="estimator_projects"),
    path("manager_projects", views.manager_projects, name="manager_projects"),
    path("approve_project/<int:project_id>", views.approve_project, name="approve_project"),
    path("reject_project/<int:project_id>", views.reject_project, name="reject_project")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)