from .zarinpal import ZarinPal
from django.http import HttpResponse
from django.shortcuts import redirect


def send_request(request):
    amount = request.GET.get('amount')
    phone = request.GET.get('phone')
    pay = ZarinPal(merchant='b7961a99-f548-4349-ad17-7cf200eb9a39',
                   call_back_url=f"http://127.0.0.1:8000/zarinpal/verify?amount={amount}")
    # email and mobile is optimal
    response = pay.send_request(amount=amount, description='توضیحات مربوط به پرداخت', email=None,
                                mobile=phone)
    if response.get('error_code') is None:
        # redirect object
        return response
    else:
        return HttpResponse(f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}')


def verify(request):
    pay = ZarinPal(merchant='b7961a99-f548-4349-ad17-7cf200eb9a39',
                   call_back_url="http://127.0.0.1:8000/zarinpal/verify")
    amount = request.GET.get('amount')
    response = pay.verify(request=request, amount=amount)

    if response.get("transaction"):
        user = request.user
        if response.get("pay"):
            user.paid = True
            user.save()
            return redirect('/?paid=success')
        else:
            user.delete()
            return redirect('sign-up/?paid=error')
    else:
        if response.get("status") == "ok":
            user.delete()
            return redirect('sign-up/?paid=error')
        elif response.get("status") == "cancel":
            user.delete()
            return redirect('sign-up/?paid=error')
