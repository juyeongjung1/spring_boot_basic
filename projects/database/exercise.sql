-- 
-- Database structure for database 'spring_exercise'
-- 
CREATE DATABASE spring_exercise CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE spring_exercise;

-- location テーブル

CREATE TABLE location (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);

INSERT INTO location (name) VALUES
('tokyo'),
('osaka'),
('fukuoka'),
('sapporo'),
('okinawa');

-- employee テーブル

CREATE TABLE employee (
    id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(50) NOT NULL,
    salary INT NOT NULL,
    location_id INT,
    FOREIGN KEY (location_id) REFERENCES location(id)
);

INSERT INTO employee (id, password, name, salary, location_id) VALUES
(1001, 'password', '山田太郎', 230000, 1),
(1002, 'password', '鈴木一郎', 230000, 2),
(1003, 'password', '田中花子', 300000, 3),
(1004, 'password', '山田次郎', 400000, 1),
(1005, 'password', '高橋美智子', 500000, 1),
(1006, 'password', '平恵', 270000, 5),
(1007, 'password', '佐々木舞', 330000, 4),
(1008, 'password', '中村翔', 350000, 3);

-- 確認用（任意）
-- SELECT e.id, e.name, l.name AS location
-- FROM employee e
-- LEFT JOIN location l ON e.location_id = l.id;

-- ユーザの作成

-- ユーザ名：spring_exercise_user
-- パスワード：password

-- GRANT ALL PRIVILEGES ON spring_exercise.* TO spring_exercise_user IDENTIFIED BY 'password';
-- GRANT ALL PRIVILEGES ON spring_exercise.* TO 'spring_exercise_user'@'localhost' IDENTIFIED BY 'password';

CREATE USER 'spring_exercise_user'@'localhost' IDENTIFIED BY 'password';
GRANT all ON spring_exercise.* TO 'spring_exercise_user'@'localhost';
FLUSH PRIVILEGES;
