from django.shortcuts import render, redirect
from django.conf import settings
from .models import PageContent,TopSearch,AffiliateProduct
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.db.models import Q
from gift.models import GiftUser  



def front(request):
    query = request.GET.get('q', '')
    products = AffiliateProduct.objects.all()

    if query:
        products = products.filter(Q(title__icontains=query) | Q(name__icontains=query))

    products = products.order_by('-id')[:30]

    context = get_common_context(request)
    context['products'] = products

    return render(request, 'front.html', context)





from .models import PageContent, TopSearch, GiftUser

def get_common_context(request):
    content = PageContent.objects.first()
    top_searches = TopSearch.objects.all()
    cart_count = request.session.get('cart_count', 0)

    user_email = None
    if request.session.get('user_id'):
        try:
            user = GiftUser.objects.get(id=request.session['user_id'])
            user_email = user.email
        except GiftUser.DoesNotExist:
            pass

    return {
        'content': content,
        'top_searches': top_searches,
        'cart_count': cart_count,
        'user_email': user_email,
    }




from django.shortcuts import render, redirect, get_object_or_404
from .models import AffiliateProduct

def confirm_payment(request, product_id):
    product = get_object_or_404(AffiliateProduct, id=product_id)
    total = product.price + product.service_fee

    if request.method == 'POST':
        method = request.POST.get('payment_method')
        # Optionally: Save the payment info to DB
        # Redirect to success page
        return redirect('payment_success')

    return render(request, 'payment.html', {
        'product': product,
        'total': total
    })




def payment_success(request):
    return render(request, 'payment_success.html')
















def register_or_login(request):
    if request.method == "POST":
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")

        try:
            user = GiftUser.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id

                # Move session cart to DB if any
                session_cart = request.session.get('cart', [])
                for pid in session_cart:
                    product = AffiliateProduct.objects.filter(id=pid).first()
                    if product:
                        Cart.objects.get_or_create(user=user, product=product)
                request.session['cart'] = []
                request.session['cart_count'] = Cart.objects.filter(user=user).count()

                messages.success(request, "Login successful")
                return redirect(request.session.pop('redirect_after_login', 'front'))

            else:
                messages.error(request, "Incorrect password.")
        except GiftUser.DoesNotExist:
            user = GiftUser(email=email)
            user.set_password(password)
            user.save()
            request.session['user_id'] = user.id
            messages.success(request, "Login successful")
            return redirect(request.session.pop('redirect_after_login', 'front'))

    return render(request, "auth/login_register.html")













from django.contrib.auth import logout

def logout_view(request):
    request.session.pop('user_id', None)
    request.session.pop('cart_count', None)
    return redirect('front')










from .models import Cart, AffiliateProduct, GiftUser
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def add_to_cart(request, product_id):
    if 'user_id' not in request.session:
        request.session['redirect_after_login'] = request.path
        return redirect('register_or_login') 

    if request.method == "POST":
        user_id = request.session['user_id']
        user = GiftUser.objects.get(id=user_id)
        product = get_object_or_404(AffiliateProduct, id=product_id)


        Cart.objects.get_or_create(user=user, product=product)


        cart_count = Cart.objects.filter(user=user).count()
        request.session['cart_count'] = cart_count

        return redirect('cart_view')

    return redirect('product_detail', product_id=product_id)







def cart_view(request):
    if 'user_id' not in request.session:
        return redirect('register_or_login')

    user_id = request.session['user_id']
    user = GiftUser.objects.get(id=user_id)

    cart_items = Cart.objects.filter(user=user).select_related('product')
    products = [item.product for item in cart_items]


    request.session['cart_count'] = cart_items.count()

    context = get_common_context(request)
    context['products'] = products
    context['cart_count'] = cart_items.count()

    return render(request, 'cart.html', context)







def remove_from_cart(request, product_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = GiftUser.objects.get(id=user_id)


        Cart.objects.filter(user=user, product_id=product_id).delete()


        request.session['cart_count'] = Cart.objects.filter(user=user).count()

    return redirect('cart_view')








 











from django.shortcuts import render, get_object_or_404


def product_detail(request, product_id):
    product = get_object_or_404(AffiliateProduct, id=product_id)


    title_keyword = product.title.split()[0] if product.title else ""
    name_keyword = product.name.split()[0] if product.name else ""


    related_products = AffiliateProduct.objects.filter(
        Q(title__icontains=title_keyword) | Q(name__icontains=name_keyword)
    ).exclude(id=product.id)[:12]


    context = get_common_context(request)
    context['product'] = product
    context['related_products'] = related_products

    return render(request, 'product_detail.html', context)










def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin.html')








def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    context = get_dashboard_context(request)
    return render(request, 'admin_dashboard.html', context)







def admin_logout(request):
    request.session.pop('admin_id', None)  
    return redirect('front')








from .models import GiftOrder

def all_orders_view(request):
    pending_orders = GiftOrder.objects.filter(status='Pending').order_by('-created_at')
    return render(request, 'pending_orders.html', {'orders': pending_orders})









from django.shortcuts import redirect, get_object_or_404
from .models import GiftOrder

def update_order_status(request, order_id, new_status):
    order = get_object_or_404(GiftOrder, id=order_id)
    order.status = new_status
    order.save()
    return redirect('all_orders_view')  








from django.shortcuts import redirect
from gift.models import GiftOrder

def delete_order(request, order_id):
    if request.method == 'POST':
        order = GiftOrder.objects.filter(id=order_id).first()
        if order:
            order.delete()
    return redirect('all_orders_view') 








from .models import GiftOrder

def approved_orders_view(request):
    approved_orders = GiftOrder.objects.filter(status='Approved').order_by('-created_at')
    return render(request, 'approved_orders.html', {'orders': approved_orders})




from django.shortcuts import render, get_object_or_404, redirect
from .models import AffiliateProduct

def admin_all_products(request):
    products = AffiliateProduct.objects.all()
    return render(request, 'edit_all_products.html', {'products': products})









from django.http import HttpResponse
from .models import AffiliateProduct, AffiliateProductImage

def edit_product(request, product_id):
    product = get_object_or_404(AffiliateProduct, id=product_id)
    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.price = request.POST.get('price')
        product.service_fee = request.POST.get('service_fee')
        product.save()
        return redirect('admin_all_products')
    
    return render(request, 'edit_product.html', {'product': product})










from django.shortcuts import render
from django.db.models import Count, Q
from django.utils.dateparse import parse_date
from gift.models import GiftOrder


from datetime import datetime, time

def get_dashboard_context(request):
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')

    start_date = parse_date(start_date_str) if start_date_str else None
    end_date = parse_date(end_date_str) if end_date_str else None

    orders = GiftOrder.objects.all()

    if start_date and end_date:

        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)
        orders = orders.filter(created_at__range=(start_datetime, end_datetime))

    total_orders = orders.count()
    pending_orders = orders.filter(status__iexact='Pending').count()
    approved_orders = orders.filter(status__iexact='Approved').count()

    return {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'approved_orders': approved_orders,
        'recent_orders': orders.order_by('-created_at')[:10],
        'start_date': start_date_str,
        'end_date': end_date_str,
    }








from django.shortcuts import redirect, get_object_or_404
from .models import GiftOrder

def update_order_status(request, order_id, new_status):
    order = get_object_or_404(GiftOrder, id=order_id)
    order.status = new_status
    order.save()
    return redirect('admin_dashboard')  











def edit_front_page(request):
    content, created = PageContent.objects.get_or_create(id=1)
    if request.method == 'POST':
        content.welcome_message = request.POST.get('welcome_message', '')
        content.about_company = request.POST.get('about_company', '')
        content.order_button_text = request.POST.get('order_button_text', '')
        content.contact_email = request.POST.get('contact_email', '')
        content.contact_phone = request.POST.get('contact_phone', '')
        content.contact_address = request.POST.get('contact_address', '')
        content.tagline = request.POST.get('tagline', '')
        content.save()
        return redirect('admin_dashboard')
    return render(request, 'edit_front.html', {'content': content})












from django.utils.text import slugify
from django.db import IntegrityError
from django.contrib import messages

def top_search_manage(request):
    top_searches = TopSearch.objects.all()
    edit_id = None
    edit_keyword = ""
    edit_url = ""

    if request.method == "POST":
        keyword = request.POST.get("top_search")
        redirect_url = request.POST.get("redirect_url", "").strip()
        slug = slugify(keyword)

        if 'add' in request.POST:
            if TopSearch.objects.filter(slug=slug).exists():
                messages.error(request, f"The keyword '{keyword}' already exists.")
            else:
                TopSearch.objects.create(keyword=keyword, slug=slug, redirect_url=redirect_url)
                

        elif 'update' in request.POST:
            keyword_id = request.POST.get("keyword_id")
            try:
                obj = TopSearch.objects.get(id=keyword_id)
                obj.keyword = keyword
                obj.slug = slug
                obj.redirect_url = redirect_url
                obj.save()
                
            except IntegrityError:
                messages.error(request, "")

        elif 'edit' in request.POST:
            keyword_id = request.POST.get("keyword_id")
            obj = TopSearch.objects.get(id=keyword_id)
            edit_id = obj.id
            edit_keyword = obj.keyword
            edit_url = obj.redirect_url

        elif 'delete' in request.POST:
            keyword_id = request.POST.get("keyword_id")
            TopSearch.objects.filter(id=keyword_id).delete()
            

    context = {
        'top_searches': top_searches,
        'edit_id': edit_id,
        'edit_keyword': edit_keyword,
        'edit_url': edit_url,
    }
    return render(request, "top_searching.html", context)









# from django.shortcuts import render, redirect
# from .models import AffiliateProduct

# def product_list(request):
#     products = AffiliateProduct.objects.all()
#     return render(request, 'add_product.html', {'products': products})






from django.contrib import messages
from django.shortcuts import render, redirect
from gift.models import AffiliateProduct, AffiliateProductImage

def add_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        service_fee = request.POST.get('service_fee')
        name = request.POST.get('name')
        image_url = request.POST.get('image_url')
        image_2 = request.POST.get('image_url_2')
        image_3 = request.POST.get('image_url_3')

        product = AffiliateProduct.objects.create(
            title=title,
            price=price,
            service_fee=service_fee,
            name=name,
            image_url=image_url,

        )

        for url in [image_2, image_3]:
            if url and url.strip():
                AffiliateProductImage.objects.create(product=product, image_url=url.strip())

        messages.success(request, 'Product added successfully!')
        return redirect('add_product') 

    return render(request, 'add_product.html')









from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from .models import AffiliateProduct, GiftOrder

def order_gift(request, product_id):
    product = get_object_or_404(AffiliateProduct, id=product_id)

    
    price = product.price or Decimal('0.00')
    service_fee = product.service_fee or Decimal('0.00')
    total = price + service_fee

    if request.method == 'POST':
        receiver_name = request.POST.get('recipient_name')
        receiver_address = request.POST.get('address')
        preferences = request.POST.get('message')
        occasion = request.POST.get('occasion')
        sender_email = request.POST.get('sender_email')
        sender_name = request.POST.get('sender_name')
        landmark = request.POST.get('landmark')
        pincode = request.POST.get('pincode')
        district = request.POST.get('district')

        GiftOrder.objects.create(
            sender_name=sender_name,
            sender_email=sender_email,
            landmark=landmark,
            pincode=pincode,
            district=district,
            receiver_name=receiver_name,
            receiver_address=receiver_address,
            preferences=preferences,
            occasion=occasion,
            product=product,
            service_fee=service_fee
        )

        return render(request, 'payment.html', {
            'product': product,
            'total': total
        })

    return render(request, 'order_gift.html', {
        'product': product,
        'price': price,
        'service_fee': service_fee,
        'total': total
    })





