import datetime as dt

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from qr_pass.settings import SEND_TELEGRAM_MESSAGE, BAD_KEY_ID, HOST_NAME
from .forms import PassForm
from .models import Customer, Logs
from .telegram import send_message


def create_key():
    return (str(dt.datetime.now())
            .replace(' ', '')
            .replace('-', '')
            .replace(':', '')
            .replace('.', '')
            )


@login_required
def index(request):
    template = 'index.html'
    var = Customer.objects.filter(master=request.user)
    form = PassForm()
    context = {
        'var': var,
        'form': form
    }
    return render(request, template, context)


@login_required
def create(request):
    form = PassForm(request.POST or None)
    if form.is_valid():
        new_rec = form.save(commit=False)
        new_rec.key = create_key()
        new_rec.master = request.user
        new_rec.save()
    return redirect('passes:index')


@login_required
def edit(request, nick):
    user = get_object_or_404(Customer, username=nick)
    if user.master == request.user:
        form = PassForm(
            request.POST or None,
            files=request.FILES or None,
            instance=user
        )
        if form.is_valid():
            form.save()
            return redirect('passes:index')
        template = 'index.html'
        var = Customer.objects.filter(master=request.user)
        context = {
            'var': var,
            'form': form,
            'is_edit': True,
            'nick': nick
        }
        return render(request, template, context)
    else:
        return redirect('passes:index')


@login_required
def delete(request, nick):
    user = get_object_or_404(Customer, username=nick)
    if user.master == request.user:
        user.delete()
    return redirect('passes:index')


@login_required
def get_qr(request, id):
    user = get_object_or_404(Customer, id=id)
    api_url = 'https://qrcode.tec-it.com/API/QRCode?data='
    my_url = f'http://{HOST_NAME}/check/'
    url = api_url + my_url + user.key + '/'
    template = 'qr.html'
    context = {
        'url': url
    }
    return render(request, template, context)


def check(request, key):
    template = 'access.html'
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
        return render(request, 'bad_qr.html')
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
    context = {
        'access': user.access,
        'name': user.real_name
    }
    return render(request, template, context)


@login_required
def logs(request):
    template = 'logs.html'
    log = Logs.objects.filter(user__master=request.user)
    context = {
        'log': log,
    }
    return render(request, template, context)
