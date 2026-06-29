# =====================================================================
# demo.py - Демонстрационный скрипт для Урока 2 ЛФМШ "Квант"
# Тема: Продвинутый Python на примере бэкенда "Сайта летней школы Квант"
# =====================================================================

import re
import time
from datetime import datetime, timezone, timedelta

# =====================================================================
# 1. args & kwargs для гибкого парсера настроек сайта
# =====================================================================
def configure_site(site_name, *flags, **settings):
    """
    Гибкий конфигуратор настроек сайта.
    *flags: Позиционные аргументы (включаемые режимы, например: DEBUG, MAINTENANCE)
    **settings: Именованные аргументы (параметры, например: port=8000, theme="light")
    """
    print(f"\n--- Конфигурация сайта '{site_name}' ---")
    print(f"Активные системные флаги (позиционные аргументы *args):")
    for flag in flags:
        print(f"  [+] Режим: {flag}")
    
    print("Пользовательские параметры сайта (именованные аргументы **kwargs):")
    for key, value in settings.items():
        print(f"  [*] {key} = {value}")
    
    return {
        "site_name": site_name,
        "flags": flags,
        "settings": settings
    }


# =====================================================================
# 2. ООП, Инкапсуляция и Свойства (User & Teacher)
# =====================================================================
class User:
    """Базовый класс пользователя сайта летней школы 'Квант'"""
    def __init__(self, username, email, role="student"):
        self.username = username
        self._email = email  # Защищенный атрибут (Protected)
        self.role = role

    @property
    def email(self):
        """Геттер для безопасного получения почты в нижнем регистре"""
        return self._email.lower()

    @email.setter
    def email(self, new_email):
        """Сеттер с валидацией почты на наличие символа '@'"""
        if "@" not in new_email:
            raise ValueError(f"Недопустимый формат email: '{new_email}'. Адрес должен содержать символ '@'.")
        self._email = new_email

    def __str__(self):
        """Строковое представление для пользователей (например, вывод в интерфейсе)"""
        return f"Пользователь {self.username} (Роль: {self.role}, Email: {self.email})"

    def __repr__(self):
        """Официальное строковое представление для разработчиков (отладка)"""
        return f"User(username='{self.username}', email='{self._email}', role='{self.role}')"


class Teacher(User):
    """Преподаватель летней школы. Наследует функционал класса User"""
    def __init__(self, username, email, subject, bio=""):
        # Вызываем конструктор базового класса User
        super().__init__(username, email, role="teacher")
        self.subject = subject  # Специализированное поле преподавателя
        self.bio = bio

    # Полиморфизм: переопределение поведения __str__
    def __str__(self):
        return f"Преподаватель {self.username} (Направление: {self.subject}, Email: {self.email})"

    def __repr__(self):
        return f"Teacher(username='{self.username}', email='{self._email}', subject='{self.subject}')"


# =====================================================================
# 3. Декоратор для проверки прав доступа пользователей (@requires_role)
# =====================================================================
def requires_role(required_role):
    """
    Параметризованный декоратор для проверки роли пользователя.
    Допускает выполнение функции только если у пользователя совпадает роль.
    """
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            # Первым аргументом декорируемой функции обязательно должен быть объект User/Teacher
            if not isinstance(user, User):
                raise TypeError("Первым аргументом должен быть передан объект класса User или его наследник.")
            
            if user.role != required_role:
                print(f"[ОТКАЗ В ДОСТУПЕ] Пользователь {user.username} (роль: {user.role}) попытался выполнить {func.__name__}. Требуется роль: {required_role}")
                return "Ошибка 403: Недостаточно прав для выполнения действия."
            
            print(f"[ДОСТУП РАЗРЕШЕН] Пользователь {user.username} успешно авторизован для действия {func.__name__}.")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


@requires_role("teacher")
def create_event(user, event_name, location):
    """Функция создания нового мероприятия (доступна только преподавателям)"""
    return f"Событие '{event_name}' в локации '{location}' успешно добавлено в базу данных."


# =====================================================================
# 4. Класс Event, Datetime и расчет наложений по времени
# =====================================================================
class Event:
    """Мероприятие в летней школе 'Квант'"""
    def __init__(self, name, speaker, start_time, duration_hours=2):
        self.name = name
        self.speaker = speaker  # Объект User или Teacher
        
        # start_time должен быть объектом datetime
        if not isinstance(start_time, datetime):
            raise TypeError("Параметр start_time должен быть объектом datetime")
            
        # Убеждаемся, что время имеет временную зону (сделаем UTC по умолчанию, если не задана)
        if start_time.tzinfo is None:
            self.start_time = start_time.replace(tzinfo=timezone.utc)
        else:
            self.start_time = start_time
            
        self.end_time = self.start_time + timedelta(hours=duration_hours)

    def is_active_at(self, check_time):
        """Проверяет, идет ли мероприятие в указанное время"""
        if check_time.tzinfo is None:
            check_time = check_time.replace(tzinfo=timezone.utc)
        return self.start_time <= check_time <= self.end_time

    def __str__(self):
        formatted_start = self.start_time.strftime("%d.%m.%Y %H:%M %Z")
        return f"Мероприятие '{self.name}' | Ведущий: {self.speaker.username} | Время: {formatted_start} (Длительность: {self.end_time - self.start_time})"

    def __repr__(self):
        return f"Event(name='{self.name}', speaker={repr(self.speaker)}, start_time='{self.start_time.isoformat()}')"


# =====================================================================
# 5. Регулярные выражения (Regex) для валидации регистраций
# =====================================================================
def validate_student_registration(username, email, phone):
    """
    Валидирует данные формы регистрации.
    - username: только латинские буквы, цифры и символ подчеркивания, от 3 до 16 символов.
    - email: стандартный формат email, оканчивающийся на домен из 2-6 букв.
    - phone: телефон в формате РФ (+79xxxxxxxxx или 89xxxxxxxxx, ровно 11 цифр).
    """
    # Шаблоны регулярных выражений
    username_pattern = r"^[a-zA-Z0-9_]{3,16}$"
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,6}$"
    phone_pattern = r"^(?:\+7|8)9\d{9}$"
    
    is_username_valid = bool(re.match(username_pattern, username))
    is_email_valid = bool(re.match(email_pattern, email))
    is_phone_valid = bool(re.match(phone_pattern, phone))
    
    errors = []
    if not is_username_valid:
        errors.append("Имя пользователя должно содержать только латинские буквы/цифры и быть от 3 до 16 символов.")
    if not is_email_valid:
        errors.append("Некорректный формат email (пример: student@kvant.ru).")
    if not is_phone_valid:
        errors.append("Телефон должен быть в формате РФ (+79XXXXXXXXX или 89XXXXXXXXX).")
        
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


# =====================================================================
# ЗАПУСК И ДЕМОНСТРАЦИЯ РАБОТЫ ВСЕХ КОМПОНЕНТОВ
# =====================================================================
if __name__ == "__main__":
    print("=== ЗАПУСК ДЕМОНСТРАЦИИ: БЭКЕНД САЙТА ЛФМШ 'КВАНТ' ===")

    # 1. Демонстрация args/kwargs
    configure_site("Сайт Кванта", "DEBUG_MODE", "SSL_ENABLED", port=443, db_host="localhost", rate_limit=60)

    # 2. Демонстрация ООП (User & Teacher)
    student = User("misha_phys", "MISHA@yandex.ru")
    teacher = Teacher("marina_math", "marina@kvant.ru", "Математический анализ", "Опыт работы в ЛФМШ 10 лет")

    print("\n--- Демонстрация ООП и инкапсуляции ---")
    print(student)  # Вызов __str__
    print(repr(student))  # Вызов __repr__
    print(teacher)  # Вызов __str__ с полиморфизмом
    
    # Работа геттера и сеттера @property
    print(f"Почта студента (после геттера lower()): {student.email}")
    try:
        student.email = "misha_new_at_yandex.ru"  # Некорректный email
    except ValueError as e:
        print(f"  [!] Ошибка валидации сеттера: {e}")
        
    student.email = "misha_new@yandex.ru"
    print(f"Почта студента изменена успешно: {student.email}")

    # 3. Демонстрация работы декоратора ролей
    print("\n--- Демонстрация работы декоратора @requires_role ---")
    # Студент пытается создать событие (будет отказ)
    res_student = create_event(student, "Лекция по квантовой физике", "Аудитория 101")
    print(f"Результат вызова для студента: {res_student}")
    
    # Преподаватель пытается создать событие (будет разрешено)
    res_teacher = create_event(teacher, "Лекция по пределам и производным", "Аудитория 302")
    print(f"Результат вызова для преподавателя: {res_teacher}")

    # 4. Демонстрация работы с Event и Datetime
    print("\n--- Демонстрация работы с расписанием (datetime) ---")
    start_dt = datetime.now(timezone.utc) + timedelta(days=1)  # Завтра в это же время
    event = Event("Матч по футболу: Преподаватели vs Студенты", teacher, start_dt, duration_hours=3)
    print(event)
    
    check_t = start_dt + timedelta(hours=1.5)  # Проверка времени в середине матча
    print(f"Идет ли матч в {check_t.strftime('%H:%M')}? {'Да' if event.is_active_at(check_t) else 'Нет'}")
    
    check_expired = start_dt + timedelta(hours=4)  # Проверка времени после окончания матча
    print(f"Идет ли матч в {check_expired.strftime('%H:%M')}? {'Да' if event.is_active_at(check_expired) else 'Нет'}")

    # 5. Демонстрация валидации регистраций (Regex)
    print("\n--- Демонстрация регулярных выражений (Regex) ---")
    valid_data = validate_student_registration("dima_sc", "dima@kvant.ru", "+79161234567")
    invalid_data = validate_student_registration("d!", "dima.com", "891234")
    
    print("Корректная регистрация:")
    print(f"  Valid: {valid_data['is_valid']}, Ошибки: {valid_data['errors']}")
    print("Некорректная регистрация:")
    print(f"  Valid: {invalid_data['is_valid']}, Ошибки: {invalid_data['errors']}")
    print("\n=======================================================")
