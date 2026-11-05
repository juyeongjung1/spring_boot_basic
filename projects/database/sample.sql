-- 
-- Database structure for database 'spring_sample'
-- 

CREATE DATABASE spring_sample CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE spring_sample;

CREATE TABLE category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES category(id)
) ENGINE=InnoDB;

CREATE TABLE user (
    emp_id INT(6) PRIMARY KEY,
    password VARCHAR(15) NOT NULL,
    emp_name VARCHAR(30) NOT NULL
) ENGINE=InnoDB;

--
-- Input Data
--

-- カテゴリテーブル
INSERT INTO category (id, name) VALUES (1, 'テレビ・モニター');
INSERT INTO category (id, name) VALUES (2, 'コンピュータ');
INSERT INTO category (id, name) VALUES (3, '冷蔵庫');
INSERT INTO category (id, name) VALUES (4, '洗濯機');

-- 商品テーブル
INSERT INTO product (name, price, category_id) VALUES ('スマートテレビ', 30000, 1);
INSERT INTO product (name, price, category_id) VALUES ('ゲーミングモニター', 20000, 1);
INSERT INTO product (name, price, category_id) VALUES ('ノートパソコン', 50000, 2);
INSERT INTO product (name, price, category_id) VALUES ('2ドア冷蔵庫', 50000, 3);
INSERT INTO product (name, price, category_id) VALUES ('コンパクト冷蔵庫', 15000, 3);
INSERT INTO product (name, price, category_id) VALUES ('ワインクーラー', 30000, 3);
INSERT INTO product (name, price, category_id) VALUES ('全自動洗濯機', 25000, 4);
INSERT INTO product (name, price, category_id) VALUES ('乾燥機能付き洗濯機', 40000, 4);
INSERT INTO product (name, price, category_id) VALUES ('洗濯乾燥機', 60000, 4);

-- 社員テーブル
INSERT INTO user (emp_id, password, emp_name) VALUES (123456, 'pass1234', '山田太郎');
INSERT INTO user (emp_id, password, emp_name) VALUES (234567, 'pass2345', '佐藤花子');
INSERT INTO user (emp_id, password, emp_name) VALUES (345678, 'pass3456', '鈴木一郎');

-- ユーザの作成

-- ユーザ名：spring_sample_user
-- パスワード：trainocate

-- GRANT ALL PRIVILEGES ON spring_sample.* TO spring_sample_userIDENTIFIED BY 'trainocate';
-- GRANT ALL PRIVILEGES ON spring_sample.* TO 'spring_sample_user'@'localhost' IDENTIFIED BY 'trainocate';

CREATE USER 'spring_sample_user'@'localhost' IDENTIFIED BY 'trainocate';
GRANT all ON spring_sample.* TO 'spring_sample_user'@'localhost';
FLUSH PRIVILEGES;
