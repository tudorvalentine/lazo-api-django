import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from LazoAPI.models import Product, Brand, Review, User

base_url = settings.MEDIA_URL


User = get_user_model()


@api_view(['POST'])
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    refresh = RefreshToken.for_user(user)

    response_data = {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(username=username).first()

    if user is None or not user.check_password(password):
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    response_data = {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    return HttpResponse("This is API for my React Native application Lazo App")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_brand(request):
    list_brands = Brand.objects.all()
    data = [{
        'brand_id': brand.id,
        'brand_name': brand.name
    } for brand in list_brands]

    return JsonResponse(data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reviews_general(request):
    count = Review.objects.all().count()
    average_rating = Review.objects.all().aggregate(Avg('rating'))
    data = {
        'count_total_review': count,
        'avg_rating': average_rating.get('rating__avg')
    }
    return JsonResponse(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    try:
        data = json.loads(request.body)
        product_id = int(data.get('product_id'))
        author_user = data.get('author_user')
        described_experience = data.get('described_experience')
        grade = data.get('grade')
        if product_id is None or author_user is None or described_experience is None or grade is None:
            return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        author = User.objects.get(id=author_user)
        product_ref = Product.objects.get(id=product_id)
        review = Review.objects.create(product=product_ref, user=author, comment=described_experience, rating=grade)
        return JsonResponse({'success': 'Review created successfully'}, status=status.HTTP_201_CREATED)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Handle other unexpected errors
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def forgot_password(request):
    email = request.GET.get('email')

    if email is None:
        return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'success': 'Forgot password'})


@api_view(['GET'])
def forgot_password_verify_code(request):
    code = request.GET.get('code')

    if code is None or code == '':
        return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    elif code == '12345':
        return Response({'success': 'Forgot password'})