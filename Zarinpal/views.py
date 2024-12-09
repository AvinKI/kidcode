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


from django.shortcuts import render, redirect
from Main.models import *
from .zarinpal import ZarinPal
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

pay = ZarinPal(
    merchant="1e80ffc0-012c-404d-bfea-4f710a64cda3",
    call_back_url="http://localhost:8000/verify/",
)
total_cost = 0
# @login_required
# def send_request(request):
#     league = League.objects.all()
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)  # Assuming UserForm handles user data
#         if user_form.is_valid():  # Validate user data
#             user = user_form.save(commit=False)  # Don't save user yet
#             # ... (extract and process user data)

#             league_ids = request.POST.getlist('league')
#             total_cost = len(league_ids) * 500000
#     if request.method == 'POST':
#         first_name = request.POST.get('name')
#         last_name = request.POST.get('last_name')
#         name_english = request.POST.get('name_english')
#         last_name_english = request.POST.get('last_name_english')
#         father_name = request.POST.get('father_name')
#         date_birth = request.POST.get('date_birth')
#         month_birth = request.POST.get('month_birth')
#         day_birth = request.POST.get('day_birth')
#         gander = request.POST.get('gander')
#         national_code = request.POST.get('national_code')
#         educational_base = request.POST.get('educational_base')
#         school_name = request.POST.get('school_name')
#         name_province = request.POST.get('mySelect')
#         number_area = request.POST.get('numberInput')
#         name_research_center_area = request.POST.get('name_research_center')
#         name_research_center1 = request.POST.get('name_research_center')
#         number_required = request.POST.get('number_required')
#         father_national_code = request.POST.get('father_national_code')
#         number_parents = request.POST.get('number_parents')
#         email = request.POST.get('email')
#         address = request.POST.get('address')
#         league_ids = request.POST.getlist('league')
#         total_cost = len(league_ids) * 5000000
#         print(total_cost)
#         response = pay.send_request(amount=total_cost, description='ثبت نام مسابقات کیدکد دانشگاه شریف', email=email,
#                                mobile=number_required)
#         if response.get('error_code') is None:
#             user = CustomUser(first_name=first_name, last_name=last_name, first_name_english=name_english,
#                           last_name_english=last_name_english, father_name=father_name,
#                           current_educational_level=educational_base, school_name=school_name,
#                           name_of_research_center=name_research_center_area, gender=gander, national_code=national_code,
#                           phone_number=number_parents, city=name_province, address=address,
#                           emergency_contact_number=number_required,
#                           fathers_national_code=father_national_code, email_address=email,
#                           parents_phone_number=number_parents, note=name_research_center1, number_area=number_area,
#                           day_of_birth=day_birth, month_of_birth=month_birth, year_of_birth=date_birth)
#             user.save()
#             leagues = League.objects.filter(id__in=league_ids)
#             user.leagues.set(leagues)
#             return('home')
#         else:
#             return HttpResponse(f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}')


# def verify(request):
#     response = pay.verify(request=request, amount=total_cost)

#     if response.get("transaction"):
#         if response.get("pay"):
#             return HttpResponse('تراکنش با موفقت انجام شد')
#         else:
#             return HttpResponse('این تراکنش با موفقیت انجام شده است و الان دوباره verify شده است')
#     else:
#         if response.get("status") == "ok":
#             return HttpResponse(f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}')
#         elif response.get("status") == "cancel":
#             return HttpResponse(f'تراکنش ناموفق بوده است یا توسط کاربر لغو شده است'
#                                 f'Error Message: {response.get("message")}')

#
# # Initialize ZarinPal instance
# pay = ZarinPal(
#     merchant="1e80ffc0-012c-404d-bfea-4f710a64cda3",
#     call_back_url="http://localhost:8000/verify/",
# )
#
#
# def send_request(request):
#     if request.method == "POST":
#         # Collect participant information from form
#         participant_data = {
#             "first_name": request.POST.get("name"),
#             "last_name": request.POST.get("last_name"),
#             "name_english": request.POST.get("name_english"),
#             "last_name_english": request.POST.get("last_name_english"),
#             "father_name": request.POST.get("father_name"),
#             "date_birth": request.POST.get("date_birth"),
#             "month_birth": request.POST.get("month_birth"),
#             "day_birth": request.POST.get("day_birth"),
#             "gander": request.POST.get("gander"),
#             "national_code": request.POST.get("national_code"),
#             "educational_base": request.POST.get("educational_base"),
#             "school_name": request.POST.get("school_name"),
#             "province": request.POST.get("mySelect"),
#             "area_number": request.POST.get("numberInput"),
#             "research_center": request.POST.get("name_research_center"),
#             "number_required": request.POST.get("number_required"),
#             "father_national_code": request.POST.get("father_national_code"),
#             "parent_phone": request.POST.get("number_parents"),
#             "email": request.POST.get("email"),
#             "address": request.POST.get("address"),
#         }
#         selected_leagues = request.POST.getlist('league')
#         selected_tendencies = request.POST.getlist('tendency')
#         print(selected_tendencies)
#         if not selected_tendencies:
#             return HttpResponse(
#                 "No league selected. Please choose at least one league.", status=400
#             )
#
#         # Calculate total cost
#         total_cost = len(selected_tendencies) * 5000000
#
#         # Initiate payment request
#         response = pay.send_request(
#             amount=total_cost,
#             description="ثبت نام مسابقات کیدکد دانشگاه شریف",
#             email=participant_data["email"],
#             mobile=participant_data["number_required"],
#         )
#
#         # Check payment initiation response
#         if response.get("error_code") is None:
#             # Save user and league details on successful payment request
#             user = CustomUser(
#                 username=participant_data["national_code"],
#                 first_name=participant_data["first_name"],
#                 last_name=participant_data["last_name"],
#                 first_name_english=participant_data["name_english"],
#                 last_name_english=participant_data["last_name_english"],
#                 father_name=participant_data["father_name"],
#                 current_educational_level=participant_data["educational_base"],
#                 school_name=participant_data["school_name"],
#                 name_of_research_center=participant_data["research_center"],
#                 gender=participant_data["gander"],
#                 national_code=participant_data["national_code"],
#                 phone_number=participant_data["parent_phone"],
#                 city=participant_data["province"],
#                 address=participant_data["address"],
#                 emergency_contact_number=participant_data["number_required"],
#                 fathers_national_code=participant_data["father_national_code"],
#                 email_address=participant_data["email"],
#                 parents_phone_number=participant_data["parent_phone"],
#                 note=participant_data["research_center"],
#                 number_area=participant_data["area_number"],
#                 day_of_birth=participant_data["day_birth"],
#                 month_of_birth=participant_data["month_birth"],
#                 year_of_birth=participant_data["date_birth"],
#             )
#             user.set_password(participant_data["national_code"])
#             user.save()
#
#             leagues = League.objects.filter(id__in=selected_leagues)
#             user.leagues.set(leagues)
#
#             return redirect(response.get("payment_url"))
#         else:
#             return HttpResponse(
#                 f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}',
#                 status=500,
#             )
#     else:
#         leagues = League.objects.all()
#         return render(request, "your_template.html", {"leagues": leagues})
#
#
# def verify(request):
#     amount = request.session.get("total_cost", 0)  # Retrieve stored amount
#
#     response = pay.verify(request=request, amount=amount)
#
#     if response.get("transaction"):
#         if response.get("pay"):
#             return HttpResponse("تراکنش با موفقیت انجام شد")
#         else:
#             return HttpResponse(
#                 "این تراکنش با موفقیت انجام شده است و الان دوباره verify شده است"
#             )
#     else:
#         if response.get("status") == "ok":
#             return HttpResponse(f'Error Message: {response.get("message")}')
#         elif response.get("status") == "cancel":
#             return HttpResponse("تراکنش ناموفق بوده است یا توسط کاربر لغو شده است")

