from django.urls import path
from . import views

urlpatterns = [
    path('', views.front, name='front'),
    path('logout/', views.logout_view, name='logout_view'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('edit-front/', views.edit_front_page, name='edit_front_page'),
    path('top-search/', views.top_search_manage, name='top_search_manage'),
    path('order/<int:product_id>/', views.order_gift, name='order_gift'),
    # path('products/', views.product_list, name='product_list'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('add-product/', views.add_product, name='add_product'),
    path('Pending_orders/', views.all_orders_view, name='all_orders_view'),
    path('update-order-status/<int:order_id>/<str:new_status>/', views.update_order_status, name='update_order_status'),
    path('approved-orders/', views.approved_orders_view, name='approved_orders'),
    path('Edit_products/', views.admin_all_products, name='admin_all_products'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('admin-dashboard/', views.get_dashboard_context, name='get_dashboard_context'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('Login/', views.register_or_login, name='register_or_login'),
    path('admin/orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('payment/<int:product_id>/', views.confirm_payment, name='confirm_payment'),

]




