import sqlite3
from datetime import datetime

def run_demo():
    # Создаем подключение к базе данных в оперативной памяти
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    print("=== Шаг 1: Создание таблиц схемы ЛШ 'Квант' ===")
    
    # Включаем поддержку внешних ключей в SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Таблица пользователей сайта
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher', 'admin'))
    );
    """)
    
    # 2. Таблица студентов (связь 1:1 с users через user_id)
    cursor.execute("""
    CREATE TABLE students (
        user_id INTEGER PRIMARY KEY,
        cohort_number INTEGER NOT NULL CHECK (cohort_number BETWEEN 1 AND 5),
        balance INTEGER DEFAULT 0 CHECK (balance >= 0),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # 3. Таблица преподавателей (связь 1:1 с users через user_id)
    cursor.execute("""
    CREATE TABLE teachers (
        user_id INTEGER PRIMARY KEY,
        subject VARCHAR(100) NOT NULL,
        bio TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # 4. Таблица мероприятий лагеря
    cursor.execute("""
    CREATE TABLE events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(150) NOT NULL,
        description TEXT,
        points INTEGER NOT NULL CHECK (points > 0),
        event_date DATE NOT NULL
    );
    """)
    
    # 5. Таблица достижений студентов (связь 1:N со students)
    cursor.execute("""
    CREATE TABLE achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        title VARCHAR(150) NOT NULL,
        points INTEGER NOT NULL CHECK (points > 0),
        awarded_at DATETIME NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(user_id) ON DELETE CASCADE
    );
    """)
    
    # 6. Таблица-связка для регистрации на мероприятия (связь N:M между students и events)
    cursor.execute("""
    CREATE TABLE event_registrations (
        student_id INTEGER NOT NULL,
        event_id INTEGER NOT NULL,
        registered_at DATETIME NOT NULL,
        PRIMARY KEY (student_id, event_id),
        FOREIGN KEY (student_id) REFERENCES students(user_id) ON DELETE CASCADE,
        FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    print("Таблицы успешно созданы.\n")
    
    print("=== Шаг 2: Вставка тестовых данных (INSERT) ===")
    
    # Добавляем пользователей
    users_data = [
        # Студенты
        ('ivan_q', 'Иван', 'Иванов', 'student'),
        ('masha_math', 'Мария', 'Петрова', 'student'),
        ('serezha_phys', 'Сергей', 'Сидоров', 'student'),
        ('dasha_art', 'Дарья', 'Козлова', 'student'),
        # Преподаватели
        ('anton_py', 'Антон', 'Программистов', 'teacher'),
        ('elena_geom', 'Елена', 'Черных', 'teacher')
    ]
    cursor.executemany("INSERT INTO users (username, first_name, last_name, role) VALUES (?, ?, ?, ?);", users_data)
    
    # Добавляем профили студентов
    students_data = [
        (1, 1, 150),
        (2, 1, 300),
        (3, 2, 50),
        (4, 2, 0)
    ]
    cursor.executemany("INSERT INTO students (user_id, cohort_number, balance) VALUES (?, ?, ?);", students_data)
    
    # Добавляем профили преподавателей
    teachers_data = [
        (5, 'Программирование на Python', 'Разработчик с 10-летним стажем, фанат Django.'),
        (6, 'Начертательная геометрия', None)
    ]
    cursor.executemany("INSERT INTO teachers (user_id, subject, bio) VALUES (?, ?, ?);", teachers_data)
    
    # Добавляем мероприятия
    events_data = [
        ('Хакатон Кванта по веб-разработке', 'Командное соревнование по созданию сайтов', 100, '2026-07-02'),
        ('Физический квест "Архимед"', 'Разгадывание загадок природы на территории лагеря', 50, '2026-07-05'),
        ('Математическая регата', 'Решение олимпиадных задач на скорость', 80, '2026-07-10')
    ]
    cursor.executemany("INSERT INTO events (title, description, points, event_date) VALUES (?, ?, ?, ?);", events_data)
    
    # Добавляем достижения студентов
    achievements_data = [
        (1, 'Победа в шахматном турнире', 50, '2026-06-28 14:00:00'),
        (1, 'Решение сложной задачи по физике', 30, '2026-06-29 11:30:00'),
        (2, 'Лучший бэкенд на Django в мини-проекте', 100, '2026-06-29 16:45:00'),
        (3, 'Активное участие на утренней зарядке', 10, '2026-06-27 08:30:00')
    ]
    cursor.executemany("INSERT INTO achievements (student_id, title, points, awarded_at) VALUES (?, ?, ?, ?);", achievements_data)
    
    # Добавляем записи студентов на мероприятия
    registrations_data = [
        (1, 1, '2026-06-29 10:00:00'),
        (1, 2, '2026-06-29 10:05:00'),
        (2, 1, '2026-06-29 10:10:00'),
        (3, 2, '2026-06-29 10:15:00')
    ]
    cursor.executemany("INSERT INTO event_registrations (student_id, event_id, registered_at) VALUES (?, ?, ?);", registrations_data)
    
    conn.commit()
    print("Тестовые данные успешно добавлены.\n")
    
    print("=== Шаг 3: Выборка и фильтрация (SELECT, WHERE, LIKE, NULL) ===")
    
    # Выберем преподавателей, у которых биография не заполнена (NULL)
    cursor.execute("""
    SELECT u.first_name, u.last_name, t.subject 
    FROM teachers t
    JOIN users u ON t.user_id = u.id
    WHERE t.bio IS NULL;
    """)
    print("Преподаватели без биографии:")
    for row in cursor.fetchall():
        print(f"- {row[0]} {row[1]} (Предмет: {row[2]})")
    print()
    
    print("=== Шаг 4: Объединение таблиц (INNER JOIN vs LEFT JOIN) ===")
    
    # INNER JOIN: выведем студентов и их достижения
    cursor.execute("""
    SELECT u.first_name, u.last_name, a.title, a.points
    FROM students s
    JOIN users u ON s.user_id = u.id
    INNER JOIN achievements a ON s.user_id = a.student_id;
    """)
    print("Студенты и их достижения (INNER JOIN):")
    for row in cursor.fetchall():
        print(f"- {row[0]} {row[1]}: {row[2]} (+{row[3]} баллов)")
    print()
    
    # LEFT JOIN: выведем ВСЕХ студентов и их достижения
    cursor.execute("""
    SELECT u.first_name, u.last_name, a.title, a.points
    FROM students s
    JOIN users u ON s.user_id = u.id
    LEFT JOIN achievements a ON s.user_id = a.student_id;
    """)
    print("Все студенты и достижения (LEFT JOIN):")
    for row in cursor.fetchall():
        ach_title = row[2] if row[2] else "Нет достижений"
        ach_points = f"+{row[3]}" if row[3] else "0"
        print(f"- {row[0]} {row[1]}: {ach_title} ({ach_points} баллов)")
    print()
    
    print("=== Шаг 5: Агрегация и Группировка (GROUP BY, HAVING) ===")
    
    # Посчитаем сумму балансов и средний баланс студентов по отрядам
    cursor.execute("""
    SELECT cohort_number, SUM(balance) as total, AVG(balance) as average, COUNT(*) as student_count
    FROM students
    GROUP BY cohort_number;
    """)
    print("Статистика по отрядам:")
    for row in cursor.fetchall():
        print(f"Отряд №{row[0]}: Всего баллов = {row[1]}, Средний балл = {row[2]:.1f}, Учеников = {row[3]}")
    print()
    
    # Группировка с фильтрацией HAVING: отряды, где средний балл студентов > 100
    cursor.execute("""
    SELECT cohort_number, AVG(balance)
    FROM students
    GROUP BY cohort_number
    HAVING AVG(balance) > 100;
    """)
    print("Отряды со средним баллом выше 100:")
    for row in cursor.fetchall():
        print(f"- Отряд №{row[0]} (Средний балл: {row[1]:.1f})")
    print()
    
    print("=== Шаг 6: Модификация данных (UPDATE, DELETE) ===")
    
    # UPDATE: Начислим 50 коинов всем студентам 2-го отряда
    print("Баланс Сергея (отряд 2) до UPDATE:", cursor.execute("SELECT balance FROM students WHERE user_id = 3;").fetchone()[0])
    cursor.execute("UPDATE students SET balance = balance + 50 WHERE cohort_number = 2;")
    print("Баланс Сергея после UPDATE:", cursor.execute("SELECT balance FROM students WHERE user_id = 3;").fetchone()[0])
    
    # DELETE: Удалим пользователя Сергея. В силу каскадного удаления,
    # автоматически удалится его запись из таблицы students, его достижения и регистрации на мероприятия!
    cursor.execute("DELETE FROM users WHERE id = 3;")
    print("\nПроверка удаления Сергея:")
    student_check = cursor.execute("SELECT * FROM students WHERE user_id = 3;").fetchone()
    ach_check = cursor.execute("SELECT * FROM achievements WHERE student_id = 3;").fetchone()
    reg_check = cursor.execute("SELECT * FROM event_registrations WHERE student_id = 3;").fetchone()
    
    print("Запись в students существует?", "Да" if student_check else "Нет (Удалена каскадно)")
    print("Достижения существуют?", "Да" if ach_check else "Нет (Удалены каскадно)")
    print("Регистрации на события существуют?", "Да" if reg_check else "Нет (Удалены каскадно)")
    
    conn.close()

if __name__ == '__main__':
    run_demo()
