from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Product

def home(request):
    products = Product.objects
    return render(request, 'products/home.html',{'products':products})

@login_required
def create(request):
    if request.method=='POST':
        if request.POST['title'] and request.POST['body'] and request.FILES['icon'] and request.FILES['Image'] and request.POST.get('url1'):
            product=Product()
            product.title=request.POST['title']
            product.body=request.POST['body']
            if request.POST.get('url1').startswith("http://") or request.POST.get('url1').startswith("https://"):
                product.url=request.POST.get('url1')
            else:
                product.url='http://'+request.POST.get('url1')
            product.icon=request.FILES['icon']
            product.image=request.FILES['Image']
            product.pub_date=timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/'+str(product.id))
        else:
            return render(request,'products/create.html',{'error':'All Feild Needed'})
    else:
        return render(request,'products/create.html')

def detail(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    return render(request,'products/detail.html',{'product':product})

@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))
