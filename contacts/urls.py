from django.urls import path
from .views import ContactList, ContactDetailView,ContactSearch


urlpatterns = [
    path('', ContactList.as_view()),
    path('<int:id>', ContactDetailView.as_view()),
    path('search',ContactSearch.as_view())
    # path('search',ContactSearch.as_view(({'get': 'list'})))
]