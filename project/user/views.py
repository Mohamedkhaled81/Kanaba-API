"""
Users Views
"""
from django.contrib.auth import login, logout

from rest_framework import viewsets, mixins, views, response, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomerSerilaizer, CustomerLoginSerializer

class CustomerRegister(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = CustomerSerilaizer


class CustomerLogin(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CustomerLoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            login(request, user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)


class CustomerLogout(views.APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return response.Response(status=status.HTTP_200_OK)
