FARAPAYAMAK_API_KEY = "YOUR_API_KEY"
FARAPAYAMAK_NUMBER = "YOUR_SENDER_NUMBER"


def send_sms(phone_number, message):
    """ارسال پیامک با استفاده از فراپیامک"""
    url = "https://rest.payamak-panel.com/api/SendSMS/SendSMS"
    data = {
        "username": "YOUR_USERNAME",
        "password": "YOUR_PASSWORD",
        "to": phone_number,
        "from": FARAPAYAMAK_NUMBER,
        "text": message,
    }
    response = requests.post(url, json=data)
    return response.status_code == 200

pay = ZarinPal(
    merchant="1e80ffc0-012c-404d-bfea-4f710a64cda3",
    call_back_url="http://localhost:8000/verify/",
)


def send_request(request):
    if request.method == "POST":
        # Collect participant information from form
        participant_data = {
            "first_name": request.POST.get("name"),
            "last_name": request.POST.get("last_name"),
            "name_english": request.POST.get("name_english"),
            "last_name_english": request.POST.get("last_name_english"),
            "father_name": request.POST.get("father_name"),
            "date_birth": request.POST.get("date_birth"),
            "month_birth": request.POST.get("month_birth"),
            "day_birth": request.POST.get("day_birth"),
            "gander": request.POST.get("gander"),
            "national_code": request.POST.get("national_code"),
            "educational_base": request.POST.get("educational_base"),
            "school_name": request.POST.get("school_name"),
            "province": request.POST.get("mySelect"),
            "area_number": request.POST.get("numberInput"),
            "research_center": request.POST.get("name_research_center"),
            "number_required": request.POST.get("number_required"),
            "father_national_code": request.POST.get("father_national_code"),
            "parent_phone": request.POST.get("number_parents"),
            "email": request.POST.get("email"),
            "address": request.POST.get("address"),
        }
        selected_leagues = request.POST.getlist('league')
        selected_tendencies = request.POST.getlist('tendency')
        print(selected_tendencies)
        if not selected_tendencies:
            return HttpResponse(
                "No league selected. Please choose at least one league.", status=400
            )

        # Calculate total cost
        total_cost = len(selected_tendencies) * 5000000

        # Initiate payment request
        response = pay.send_request(
            amount=total_cost,
            description="ثبت نام مسابقات کیدکد دانشگاه شریف",
            email=participant_data["email"],
            mobile=participant_data["number_required"],
        )

        # Check payment initiation response
        if response.get("error_code") is None:
            # Save user and league details on successful payment request
            user = CustomUser(
                username=participant_data["national_code"],
                first_name=participant_data["first_name"],
                last_name=participant_data["last_name"],
                first_name_english=participant_data["name_english"],
                last_name_english=participant_data["last_name_english"],
                father_name=participant_data["father_name"],
                current_educational_level=participant_data["educational_base"],
                school_name=participant_data["school_name"],
                name_of_research_center=participant_data["research_center"],
                gender=participant_data["gander"],
                national_code=participant_data["national_code"],
                phone_number=participant_data["parent_phone"],
                city=participant_data["province"],
                address=participant_data["address"],
                emergency_contact_number=participant_data["number_required"],
                fathers_national_code=participant_data["father_national_code"],
                email_address=participant_data["email"],
                parents_phone_number=participant_data["parent_phone"],
                note=participant_data["research_center"],
                number_area=participant_data["area_number"],
                day_of_birth=participant_data["day_birth"],
                month_of_birth=participant_data["month_birth"],
                year_of_birth=participant_data["date_birth"],
            )
            user.set_password(participant_data["national_code"])
            user.save()

            leagues = League.objects.filter(id__in=selected_leagues)
            user.leagues.set(leagues)

            return redirect(response.get("payment_url"))
        else:
            return HttpResponse(
                f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}',
                status=500,
            )
    else:
        leagues = League.objects.all()
        return render(request, "your_template.html", {"leagues": leagues})


def verify(request):
    amount = request.session.get("total_cost", 0)  # Retrieve stored amount

    response = pay.verify(request=request, amount=amount)

    if response.get("transaction"):
        if response.get("pay"):
            return HttpResponse("تراکنش با موفقیت انجام شد")
            try:

                message = "شما با موفقیت ثبت‌نام شدید. به وب‌سایت ما خوش آمدید!"
                send_sms(phone_number, message)

                messages.success(request, "Registration successful! SMS sent.")
                return redirect("login")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect("register")

        else:
            return HttpResponse(
                "این تراکنش با موفقیت انجام شده است و الان دوباره verify شده است"
            )
    else:
        if response.get("status") == "ok":
            return HttpResponse(f'Error Message: {response.get("message")}')
        elif response.get("status") == "cancel":
            return HttpResponse("تراکنش ناموفق بوده است یا توسط کاربر لغو شده است")


