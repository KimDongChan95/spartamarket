from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Wishlist
from django.shortcuts import render, redirect, get_object_or_404


def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.liked_by.all():
        product.liked_by.remove(request.user)  # 이미 찜한 경우 취소
    else:
        product.liked_by.add(request.user)  # 찜하기 추가
    return redirect('profile', username=request.user.username)

def product_list(request):
    products = Product.objects.all()  # 모든 상품 가져오기
    return render(request, 'products/product_list.html', {'products': products})  # 템플릿 렌더링

def profile(request, username):
    user = get_object_or_404(User, username=username)
    products = user.products.all()  # 등록한 물건
    liked_products = user.liked_products.all()  # 찜한 물건
    return render(request, 'profile.html', {
        'user': user,
        'products': products,  # 등록한 물건
        'liked_products': liked_products,  # 찜한 물건
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

# 2. 상품 상세 페이지
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_liked = request.user.is_authenticated and product.liked_by.filter(id=request.user.id).exists()
    wishlist_items = Wishlist.objects.filter(user=request.user)  # 현재 사용자의 찜 목록 가져오기

    return render(request, 'products/product_detail.html', {
        'product': product,
        'is_liked': is_liked,
        'wishlist_items': wishlist_items,  # 찜 목록 전달
    })

# 3. 상품 등록
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

# 4. 상품 수정
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.created_by:  # 작성자만 수정 가능
        return redirect('product_list')  # 권한이 없으면 리스트로 이동

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)  # 수정 후 상세 페이지로 이동
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

# 5. 상품 삭제
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user == product.created_by:  # 작성자만 삭제 가능
        product.delete()  # 삭제 실행
    return redirect('product_list')  # 삭제 후 리스트로 이동

# 6. 찜하기/찜 취소
@login_required
def toggle_like(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user in product.liked_by.all():
        product.liked_by.remove(request.user)
    else:
        product.liked_by.add(request.user)
    # 찜하기/찜 취소 후 상세 페이지로 리다이렉트
    return redirect('product_detail', pk=pk)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        print(f"[DEBUG] 찜 추가됨: {wishlist_item.product.name} by {request.user.username}")
    else:
        print(f"[DEBUG] 이미 찜한 상품: {wishlist_item.product.name} by {request.user.username}")
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    print(f"찜 취소됨: {product.name} by {request.user.username}")
    return redirect('wishlist')

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'products/wishlist.html', {'wishlist_items': wishlist_items})

