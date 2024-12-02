from Main.models import *


def greeting_message(request):
    information = Information.objects.first()
    home_data = HomePage.objects.first()
    return {'information': information ,'home_data':home_data}
