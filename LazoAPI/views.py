from django.conf import settings
from django.db.models import Max
from django.http import JsonResponse, HttpResponse

from LazoAPI.models import Product, Brand, Review


def index(request):
    return HttpResponse("This is API for my React Native application Lazo App")


def products(request):
    offset = int(request.GET.get('offset'))
    limit = int(request.GET.get('limit'))

    list_product = Product.objects.all().order_by('id')[offset: offset + limit]
    data = [{
        'product_id': product.id,
        'product_name': product.name,
        'price': product.price
    } for product in list_product]
    return JsonResponse(data, safe=False)


def product_detail(request):
    id = int(request.GET.get('id'))

    product = Product.objects.get(id=id)
    top_rated_review = Review.objects.filter(product=product).aggregate(Max('rating'))

    base_url = settings.MEDIA_URL

    data = {
        'id_product': product.id,
        'product_type': product.type,
        'product_name': product.name,
        'price': product.price,
        'cover_image': f"{base_url}{product.cover_image.name}",
        'product_angles': [f"{base_url}{angle.name}"
                           for angle in
                           [
                               product.angle1,
                               product.angle2,
                               product.angle3,
                               product.angle4
                           ]
                           ],
        'description': product.description
    }
    return JsonResponse(data)


def brand(request):
    list_brands = Brand.objects.all()
    data = [{
        'brand_id': brand.id,
        'brand_name': brand.name
    } for brand in list_brands]

    return JsonResponse(data, safe=False)
