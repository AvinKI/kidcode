from Main.models import *
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def sign_up(request):
    league = Field.objects.prefetch_related('leagues').all()

    if request.method == 'POST':
        first_name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        name_english = request.POST.get('name_english')
        last_name_english = request.POST.get('last_name_english')
        father_name = request.POST.get('father_name')
        date_birth = request.POST.get('date_birth')
        month_birth = request.POST.get('month_birth')
        day_birth = request.POST.get('day_birth')
        gander = request.POST.get('gander')
        national_code = request.POST.get('national_code')
        educational_base = request.POST.get('educational_base')
        school_name = request.POST.get('school_name')
        name_province = request.POST.get('mySelect')
        number_area = request.POST.get('numberInput')
        name_research_center_area = request.POST.get('name_research_center')
        name_research_center1 = request.POST.get('name_research_center')
        number_required = request.POST.get('number_required')
        father_national_code = request.POST.get('father_national_code')
        number_parents = request.POST.get('number_parents')
        email = request.POST.get('email')
        address = request.POST.get('address')
        league_ids = request.POST.getlist('tendencies') or []


        user = CustomUser(username=national_code, first_name=first_name, last_name=last_name,
                          first_name_english=name_english,
                          last_name_english=last_name_english, father_name=father_name,
                          current_educational_level=educational_base, school_name=school_name,
                          name_of_research_center=name_research_center_area, gender=gander, national_code=national_code,
                          phone_number=number_parents, city=name_province, address=address,
                          emergency_contact_number=number_required,
                          fathers_national_code=father_national_code, email=email,
                          parents_phone_number=number_parents, note=name_research_center1, number_area=number_area,
                          day_of_birth=day_birth, month_of_birth=month_birth, year_of_birth=date_birth)
        user.set_password(national_code)

        user.save()
        login(request, user)

        leagues = Field.objects.filter(id__in=league_ids)
        user.leagues.set(leagues.values_list('id', flat=True))

        return redirect('home')

    return render(request, 'sign-up.html', {'leagues': league})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard_student(request):
    user = request.user
    user_leagues = user.leagues.all()

    other_users = CustomUser.objects.filter(leagues__in=user_leagues).exclude(id=user.id).distinct()
    other_users_count = other_users.count()
    context = {
        'user': user,
        'page_data' : StudentDashboard.objects.first(),
        'other_users': other_users_count,
    }
    return render(request, 'index-student.html', context)



@login_required
def profile_setting(request):
    user = request.user

    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            request.user.profile_picture.save(profile_picture.name, ContentFile(profile_picture.read()))
            request.user.save()
        return redirect('dashboard_student')
    return render(request, 'pages-account-settings-account.html', {'user':user})
