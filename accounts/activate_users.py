from django.contrib.auth.models import User

def activate_user(username):
    user = User.objects.get(username=username)
    if not user.is_active:
        user.is_active = True
        user.save()
    print(f"User '{user.username}' is_active: {user.is_active}")

# Пример вызова функции
activate_user('your_username')  # Замените 'your_username' на имя пользователя
