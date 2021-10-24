from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("account", views.view_user, name="view_user"),
    path("account/edit", views.edit_user, name="edit_user"),
    path("list", views.bank_list_view, name="bank_list_view"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create", views.create, name="create"),
    path("bank/<int:bank_id>", views.bank_view, name="bank"),
    path("bank/<int:bank_id>/json", views.get_bank_json, name="get_bank_json"),
    path("bank/<int:bank_id>/ticket", views.create_ticket, name="create_ticket"),
    path("about", views.about, name='about'),
    path("mybanks", views.my_foodbanks_view, name="my_foodbanks_view"),
    path("mybank/<int:bank_id>", views.my_foodbank_view, name="my_foodbank_view"),
    path("mybank/<int:bank_id>/tickets", views.tickets_view, name="tickets_view"),
    path("mybank/<int:bank_id>/tickets/<int:ticket_id>", views.view_ticket, name="view_ticket"),
    path("mybank/<int:bank_id>/edit", views.edit_bank, name="edit_bank"),
]
