from django.conf import settings
from django.db.models import Avg
from django.http import JsonResponse, HttpResponse

from LazoAPI.models import Product, Brand, Review, User

base_url = settings.MEDIA_URL


def index(request):
    return HttpResponse("This is API for my React Native application Lazo App")


def get_products(request):
    offset = int(request.GET.get('offset'))
    limit = int(request.GET.get('limit'))

    list_product = Product.objects.all().order_by('id')[offset: offset + limit]
    data = [{
        'product_id': product.id,
        'product_name': product.name,
        'price': product.price
    } for product in list_product]
    return JsonResponse(data, safe=False)


def get_product_detail(request):
    id = int(request.GET.get('id'))

    product = Product.objects.get(id=id)
    top_rated_review = Review.objects.filter(product=product).order_by('-rating').first()


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
        'description': product.description,
        'top_rated_review': {
            'author_review': top_rated_review.user.username,
            'date': top_rated_review.date_added.strftime('%d %b, %Y'),
            'rating': top_rated_review.rating,
            'review_text': top_rated_review.comment
        } if top_rated_review else None
    }
    return JsonResponse(data)


def get_brand(request):
    list_brands = Brand.objects.all()
    data = [{
        'brand_id': brand.id,
        'brand_name': brand.name
    } for brand in list_brands]

    return JsonResponse(data, safe=False)


def get_reviews_general(request):
    count = Review.objects.all().count()
    average_rating = Review.objects.all().aggregate(Avg('rating'))
    data = {
        'count_total_review': count,
        'avg_rating': average_rating.get('rating__avg')
    }
    return JsonResponse(data)


def get_reviews(request):
    product_id = int(request.GET.get('product_id'))
    offset = int(request.GET.get('offset'))
    limit = int(request.GET.get('limit'))

    product = Product.objects.get(id=product_id)
    list_reviews = Review.objects.filter(product=product)

    data = [{
        'author_avatar_uri': f'{base_url}{User.objects.get(username=review.user).avatar}',
        'author_name': f'{User.objects.get(username=review.user).username}',
        'rating': review.rating,
        'post_date': review.date_added.strftime('%d %b, %Y'),
        'review_text': review.comment
    } for review in list_reviews]

    return JsonResponse(data, safe=False)

