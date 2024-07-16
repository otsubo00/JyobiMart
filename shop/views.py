from django.views import View
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from shop.models import Product, Cart, Order, OrderDetail
from django.shortcuts import redirect


# Create your views here.
class IndexView(TemplateView):
    template_name = "shop/index.html"


class ProductSearchView(View):
    def get(self, request, *args, **kwargs):
        # 商品を検索する
        category_id = request.GET.get("c")
        keyword = request.GET.get("k")

        # カテゴリーが選択されていない場合、全ての商品を検索する
        # カテゴリーが選択されている場合、カテゴリーに紐づく商品を検索する
        if category_id == "0":
            Product_list = Product.objects.filter(name__icontains=keyword)
        else:
            print("else:", category_id)
            Product_list = Product.objects.filter(category_id=category_id, name__icontains=keyword)

        context = {
            "Product_list": Product_list,
            "keyword": keyword,
        }

        return TemplateResponse(request, "shop/product_search.html", context)


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        # 商品の詳細を取得
        product_id = kwargs["product_id"]
        product = Product.objects.get(id=product_id)

        context = {
            "product": product,
        }

        return TemplateResponse(request, "shop/product_detail.html", context)


class CartView(View):
    def get(self, request, *args, **kwargs):
        # カート内の商品を取得
        cart_list = Cart.objects.prefetch_related("product_id").filter(user_id=request.user)

        # カート内の商品の在庫数が変更された場合、カート内の数量を在庫数に合わせる
        # カート内の数量が0の場合、カートから削除する
        for item in cart_list:
            if item.product_id.stock < item.quantity or item.quantity == 0:
                item.delete()
                cart_list = Cart.objects.prefetch_related("product_id").filter(user_id=request.user)

        cart_all_quantity = sum(item.quantity for item in cart_list)
        total_price = sum(item.product_id.price * item.quantity for item in cart_list)

        context = {
            "cart_list": cart_list,
            "cart_all_quantity": cart_all_quantity,
            "total_price": total_price,
        }

        return TemplateResponse(request, "shop/cart.html", context)


class AddCartView(View):
    def get(self, request, *args, **kwargs):
        print("AddToCartView")
        # カートに商品を追加する
        product_id = kwargs["product_id"]
        quantity = int(request.GET.get("q"))
        cart_list = Cart.objects.filter(user_id=request.user, product_id=product_id)

        # カート内に同じ商品がある場合、数量を1増やす
        # カート内に同じ商品がない場合、新しくカートに追加する
        if cart_list.exists():
            cart = cart_list.first()
            cart.quantity += quantity
            cart.save()
        else:
            Cart.objects.create(
                user_id=request.user,
                product_id=Product.objects.get(id=product_id),
                quantity=quantity
            )

        # 前のページにリダイレクトする
        return redirect("shop:cart")


class UpdateCartView(View):
    def post(self, request, *args, **kwargs):
        print("update_quantity")
        # カート内の商品の数量を変更する
        product_id = kwargs["product_id"]
        quantity = int(request.POST.get("quantity"))
        cart = Cart.objects.get(user_id=request.user, product_id=product_id)
        cart.quantity = quantity
        cart.save()

        return redirect("shop:cart")


class DeleteCartView(View):
    def get(self, request, *args, **kwargs):
        # カート内の商品を削除する
        product_id = kwargs["product_id"]
        cart = Cart.objects.get(user_id=request.user, product_id=product_id)
        cart.delete()

        return redirect("shop:cart")


class OrderView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        cart_list = Cart.objects.filter(user_id=user)
        total_price = sum(item.product_id.price * item.quantity for item in cart_list)

        return TemplateResponse(request, "shop/order.html", {'user': user, 'cart_list': cart_list, 'total_price': total_price})

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_list = Cart.objects.filter(user_id=user)

        # 注文モデルにデータを登録する
        order = Order.objects.create(
            user_id=user,
            total_price=sum(item.product_id.price * item.quantity for item in cart_list)
        )
        for item in cart_list:
            OrderDetail.objects.create(
                order_id=order,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product_id.price
            )

        # カートをクリア
        cart_list.delete()
        return redirect('shop:order_complete')


class OrderCompleteView(View):
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, "shop/order_complete.html")


index = IndexView.as_view()
product_search = ProductSearchView.as_view()
product_detail = ProductDetailView.as_view()
cart = CartView.as_view()
add_cart = AddCartView.as_view()
update_cart = UpdateCartView.as_view()
delete_cart = DeleteCartView.as_view()
order = OrderView.as_view()
order_complete = OrderCompleteView.as_view()
