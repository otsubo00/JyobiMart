from .models import Category, Cart

def header_context(request):
    return {
        'cart_count': Cart.objects.filter(user_id=request.user).count() if request.user.is_authenticated else 0,
        'categories': Category.objects.all()
    }