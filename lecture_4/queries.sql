-- Создание таблицы студентов
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_year INTEGER
);

-- Создание таблицы оценок
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Вставка данных
BEGIN TRANSACTION;

INSERT INTO students (full_name, birth_year) VALUES 
    ("Alice Johnson", 2005),
    ("Brian Smith", 2004),
    ("Carla Reyes", 2006),
    ("Daniel Kim", 2005),
    ("Eva Thompson", 2003),
    ("Felix Nguyen", 2007),
    ("Grace Patel", 2005),
    ("Henry Lopez", 2004),
    ("Isabella Martinez", 2006);

INSERT INTO grades (student_id, subject, grade) VALUES 
    (1, "Math", 88), (1, "English", 92), (1, "Science", 85),
    (2, "Math", 75), (2, "History", 83), (2, "English", 79),
    (3, "Science", 95), (3, "Math", 91), (3, "Art", 89),
    (4, "Math", 84), (4, "Science", 88), (4, "Physical Education", 93),
    (5, "English", 90), (5, "History", 85), (5, "Math", 88),
    (6, "Science", 72), (6, "Math", 78), (6, "English", 81),
    (7, "Art", 94), (7, "Science", 87), (7, "Math", 90),
    (8, "History", 77), (8, "Math", 83), (8, "Science", 80),
    (9, "English", 96), (9, "Math", 89), (9, "Art", 92);

COMMIT;

-- СОЗДАНИЕ ИНДЕКСОВ ДО ВЫПОЛНЕНИЯ ЗАПРОСОВ

-- Для ускорения поиска по имени студента
CREATE INDEX IF NOT EXISTS idx_students_full_name ON students(full_name);

-- Для ускорения JOIN и фильтрации по студенту
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);

-- Для ускорения поиска по году рождения
CREATE INDEX IF NOT EXISTS idx_students_birth_year ON students(birth_year);

-- Для ускорения поиска по оценке
CREATE INDEX IF NOT EXISTS idx_grades_grade ON grades(grade);

-- Для ускорения группировки по предмету
CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject);

-- ЗАПРОСЫ

-- Оценки Alice Johnson
SELECT g.subject, g.grade 
FROM grades g
JOIN students s ON g.student_id = s.id
WHERE s.full_name = "Alice Johnson"
ORDER BY g.grade;

-- Средний балл каждого студента
SELECT s.full_name, 
       ROUND(AVG(g.grade), 2) AS avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.full_name
ORDER BY avg_grade DESC;

-- Студенты, родившиеся после 2004 года
SELECT full_name 
FROM students 
WHERE birth_year > 2004;

-- Средний балл по предметам
SELECT subject, 
        ROUND(AVG(grade), 2) AS avg_grade 
FROM grades 
GROUP BY subject 
ORDER BY avg_grade DESC;

-- Топ-3 студента по среднему баллу
SELECT s.full_name, 
        ROUND(AVG(g.grade), 2) AS avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.full_name
ORDER BY avg_grade DESC 
LIMIT 3;

-- Студенты с хотя бы одной оценкой ниже 80
SELECT s.full_name
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE EXISTS(SELECT 1
             FROM grades g2 
             WHERE g2.student_id = s.id 
             AND g2.grade < 80)
GROUP BY s.full_name;