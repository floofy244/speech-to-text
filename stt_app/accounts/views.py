from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serializers import userSerializer, userRegisterationSerializer, userProfileSerializer

user = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = userRegisterationSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user' : userSerializer(user).data,
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
        }, status = status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes({AllowAny})
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            'error' : 'Please provide both username and password!'
        }, status = status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username = username, password = password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user' : userSerializer(user).data,
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
        })
    else:
        return Response({
            'error' : 'Invalid Credentials'
        }, status = status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    serializer = userSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    serializer = userProfileSerializer(request.user, data = request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(userSerializer(request.user).data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_quota(request):
    user = request.user
    remaining_quota = user.get_remaining_quota()

    return Response({
        'remaining_minutes' : float(remaining_quota),
        'total_quota' : float(user.monthly_quota_minutes),
        'used_minutes' : float(user.minutes_processed),
        'total_cost' : float(user.total_cost),
    })
