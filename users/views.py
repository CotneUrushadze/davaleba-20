from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from users.serializers import UserSerializer, RegisterSerializar
from users.models import User
from rest_framework.permissions import IsAuthenticated
from products.permissions import IsObjectOwnerOrReadOnly
from .serializers import ProfileSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class RegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializar





class ProfileViewSet(RetrieveModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,
                      GenericViewSet):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(profile__user=self.request.user)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.profile.user != self.request.user:
            raise PermissionDenied("you do not have permission to update this")
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    

    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied("you do not have permission to delete this")
        instance.delete()
