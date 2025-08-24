from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from notifications.models import Notification


class RegisterView(generics.CreateAPIView):
    """User registration view"""
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """User login view"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """User profile view"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """Follow a user"""
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    
    if user_to_follow == request.user:
        return Response(
            {'error': 'You cannot follow yourself'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.following.add(user_to_follow)
    
    # Create notification for the followed user
    Notification.objects.create(
        recipient=user_to_follow,
        actor=request.user,
        verb='started following you',
        target=request.user
    )
    
    return Response(
        {'message': f'You are now following {user_to_follow.username}'}, 
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """Unfollow a user"""
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    
    if user_to_unfollow == request.user:
        return Response(
            {'error': 'You cannot unfollow yourself'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.following.remove(user_to_unfollow)
    return Response(
        {'message': f'You have unfollowed {user_to_unfollow.username}'}, 
        status=status.HTTP_200_OK
    )
