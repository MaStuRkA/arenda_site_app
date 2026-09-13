'''
    Файл utils.py (сокращение от англ. utilities — утилиты, вспомогательные инструменты) нужен для хранения вспомогательного кода,
    который выполняет небольшие,
    изолированные задачи и часто используется в
    разных частях проекта.
'''

def get_client_ip(request):
    """Возвращает реальный IP-адрес пользователя."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print(x_forwarded_for)
    if x_forwarded_for:
        # Берём самый первый IP из списка и очищаем его от пробелов
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip