from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet,
    BookViewSet,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    BookListView,
)
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books_all', BookViewSet, basename='book_all')


urlpatterns = [
    # Router endpoints for ViewSets
    path('', include(router.urls)),

    # Generic views endpoints
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/list/', ListView.as_view(), name='book-list-readonly'),
    path('books/create/', CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),

    # Token authentication endpoint
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]