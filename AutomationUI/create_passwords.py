from django.contrib.auth.models import User


def create_pass():
    users= User.objects.all()
    for u_obj in users:
        pass_val = u_obj.username.split('.')[0] +'@12345'
        u_obj.set_password(pass_val)
        u_obj.save()

create_pass()