
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    directive = models.FileField(upload_to='directive')

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    directive = models.FileField(upload_to='directive')


    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=50)
    league = models.ForeignKey(Field, on_delete=models.CASCADE ,  related_name='leagues')
    cost = models.IntegerField(default=0)
    possibility_of_group_registration = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Supporter(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logo')

    def __str__(self):
        return self.name


class HomePage(models.Model):
    title = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to='home')
    url = models.URLField()
    author = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='home')
    job_title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Information(models.Model):
    phone_number = models.IntegerField(blank=False)
    email_address = models.EmailField(blank=True)
    address = models.TextField(blank=False)
    footer_label = models.CharField(max_length=50, blank=False)
    footer_text = models.CharField(max_length=50, blank=False)
    footer_label_2 = models.CharField(max_length=50, blank=True)
    footer_text_2 = models.CharField(max_length=50, blank=True)
    footer_label_3 = models.CharField(max_length=50, blank=True)
    footer_text_3 = models.CharField(max_length=50, blank=True)
    location = models.URLField(blank=True)
    tel_link = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and Information.objects.exists():
            raise ValidationError('There can only be one Information instance')
        return super(Information, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError('Cannot delete Information instance')


class Slide(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='slide')

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    first_name_english = models.CharField(max_length=20, blank=True)
    last_name_english = models.CharField(max_length=20, blank=True)
    father_name = models.CharField(max_length=20, blank=True)
    current_educational_level = models.CharField(max_length=20, blank=True)
    school_name = models.TextField(blank=True)
    name_of_research_center = models.CharField(max_length=90, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    national_code = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=30, blank=True)
    emergency_contact_number = models.CharField(max_length=15, default="0000000000")
    fathers_national_code = models.CharField(max_length=10, null=False, blank=False)
    note = models.CharField(null=True, blank=True, max_length=90)
    address = models.TextField(blank=True)
    parents_phone_number = models.IntegerField(blank=True, default="0000000000")
    leagues = models.ManyToManyField(League, verbose_name="League")
    year_of_birth = models.CharField(blank=True, max_length=4)
    month_of_birth = models.CharField(blank=True, max_length=25)
    day_of_birth = models.CharField(blank=True, max_length=13)
    number_area = models.IntegerField(blank=True, default=1)
    paid = models.BooleanField(verbose_name="پرداخت شده", default=False)
    profile_photo = models.ImageField(blank=True , null=True , upload_to='profile')
    registration_type = models.CharField(max_length=20, blank=True , choices={'انفرادی':'انفرادی','تیمی':'تیمی'} , default='انفرادی')
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",
        blank=True,
        help_text="Specific permissions for this user."
    )


class Alert(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()


class StudentDashboard(models.Model):
    teacher = models.CharField(blank=True , default='10' , max_length=3)
    title_step_one = models.CharField(blank=True , max_length=100)
    text_step_one = models.CharField(blank=True , max_length=200)
    title_step_two = models.CharField(blank=True , max_length=100)
    text_step_two = models.CharField(blank=True , max_length=200)
    title_step_three = models.CharField(blank=True , max_length=100)
    text_step_tree = models.CharField(blank=True , max_length=200)
    title_step_four = models.CharField(blank=True , max_length=100)
    text_step_four = models.CharField(blank=True , max_length=200)
    title_step_five = models.CharField(blank=True , max_length=100)
    text_step_five= models.CharField(blank=True , max_length=200)
    title_step_six = models.CharField(blank=True , max_length=100)
    text_step_six= models.CharField(blank=True , max_length=200)
    title_step_seven = models.CharField(blank=True , max_length=100)
    text_step_seven= models.CharField(blank=True , max_length=200)

class Commment(models.Model):
    name = models.CharField(max_length=50 , blank=False)
    text = models.TextField(blank=False)
    profile = models.ImageField(upload_to='profile_cm/')


class ContactUsForm(models.Model):
    email = models.EmailField(verbose_name='ایمیل',blank=True)
    subject = models.CharField(max_length=100,blank=True, verbose_name='موضوع پیام')
    message = models.TextField(verbose_name='متن پیام' , blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال' , blank=True , null=True)

    def __str__(self):
        return f"{self.subject} - {self.email}"