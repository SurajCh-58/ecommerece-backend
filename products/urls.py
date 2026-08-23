from django.urls import path
from products.views import ProductView,CategoryView,ProductDetailView,RelatedProductsView
urlpatterns = [
    path('products/',ProductView.as_view(),name="products"),
    path('categories/',CategoryView.as_view(),name="category"),
    path('product/<slug:product_slug>',ProductDetailView.as_view(),name="product"),
    path('products/<slug:product_slug>/related',RelatedProductsView.as_view(),name="related_products"),
]
