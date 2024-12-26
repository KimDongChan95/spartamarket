from django.urls import path
from . import views  # views 파일에서 가져오기

urlpatterns = [
    path('', views.product_list, name='product_list'),  # 상품 목록 URL
    path('product/<int:product_id>/like/', views.like_product, name='like_product'),  # 찜하기 URL
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
]