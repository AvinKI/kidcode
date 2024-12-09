from django.db import models
from django.contrib.auth.models import User
from Main.models import *

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام تیم")
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="لیگ")
    leader = models.ForeignKey(CustomUser, related_name="led_teams", on_delete=models.CASCADE, verbose_name="سرگروه")
    members = models.ManyToManyField(CustomUser, related_name="teams", blank=True, verbose_name="اعضا")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"{self.name} - لیگ: {self.league.name}"



class Invitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="تیم")
    invited_user = models.ForeignKey(CustomUser, related_name="invitations", on_delete=models.CASCADE, verbose_name="کاربر دعوت‌شده")
    inviter = models.ForeignKey(CustomUser, related_name="sent_invitations", on_delete=models.CASCADE, verbose_name="دعوت‌کننده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال دعوت‌نامه")
    accepted = models.BooleanField(default=False, verbose_name="پذیرفته شده")

    def __str__(self):
        return f"دعوت‌نامه از {self.inviter} به {self.invited_user} برای تیم {self.team.name}"