import datetime as dt
import uuid

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from qpass.models import Customer, Logs, Device
from qr_pass.settings import BAD_KEY_ID, HOST_NAME, SEND_TELEGRAM_MESSAGE
from qpass.telegram import send_message
from .serializer import CustomerViewSerializer, LogsViewSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerViewSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        queryset = Customer.objects.filter(master=request.user)
        serializer = CustomerViewSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(Customer, pk=self.kwargs.get('pk'))
        if request.user != user.master:
            return Response('Не могу показать.',
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(Customer, pk=self.kwargs.get('pk'))
        if request.user != user.master:
            return Response('Не могу изменить',
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        user = get_object_or_404(Customer, pk=self.kwargs.get('pk'))
        if request.user != user.master:
            return Response('Не могу изменить',
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(Customer, pk=self.kwargs.get('pk'))
        if request.user != user.master:
            return Response('Не могу удалить этого посетителя.',
                            status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response('OK')


class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsViewSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = Logs.objects.filter(user__master=request.user)
        serializer = LogsViewSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_qr(request, id):
    user = get_object_or_404(Customer, id=id)
    if request.user != user.master or user.id == BAD_KEY_ID:
        return Response('Не могу создать код для этого пользователя.',
                        status=status.HTTP_400_BAD_REQUEST)
    api_url = 'https://qrcode.tec-it.com/API/QRCode?data='
    my_url = f'http://{HOST_NAME}/check/'
    url = api_url + my_url + user.key + '/'
    return Response({'qr_image': url})


@api_view(['get'])
@permission_classes([IsAuthenticated])
def check(request, key):
    try:
        user = get_object_or_404(Customer, key=key)
    except Exception:
        if SEND_TELEGRAM_MESSAGE:
            send_message(
                f'Попытка использовать неверный код: {key} в: '
                f'{str(dt.datetime.now())[:-7]}'
            )
        user = get_object_or_404(Customer, id=BAD_KEY_ID)
        Logs.objects.create(
            user=user,
            success=False,
            visit=str(dt.datetime.now())[:-7]
        )
        return Response(f'Попытка использовать неверный код {key}',
                        status=status.HTTP_400_BAD_REQUEST)
    Logs.objects.create(user=user, success=user.access)
    message = (
            'Доступ запросил: ' +
            str(user.real_name) +
            '(' + str(user) + '), ' +
            'получил доступ: ' + str(user.access) +
            ', в: ' + str(dt.datetime.now())[:-7]
    )
    if SEND_TELEGRAM_MESSAGE:
        send_message(message)

    if user.access:
        return Response({'access': True, 'user': user.real_name},
                        status=status.HTTP_200_OK)
    return Response({'access': False, 'user': user.real_name},
                    status=status.HTTP_200_OK)


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_dev_id(request):
    dev_id = str(uuid.uuid4())
    Device.objects.create(dev_id=dev_id)
    return Response({'dev_id': dev_id})
