SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS shopkeeper_dw
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

USE shopkeeper_dw;

CREATE TABLE dim_region (
    region_id INT PRIMARY KEY,
    province VARCHAR(50) NOT NULL,
    region_name VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL
);
INSERT INTO dim_region (region_id, province, region_name, country) VALUES
(1, '江苏省', '华东', '中国'),
(2, '浙江省', '华东', '中国'),
(3, '广东省', '华南', '中国'),
(4, '四川省', '西南', '中国'),
(5, '北京市', '华北', '中国');

CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    member_level VARCHAR(20) NOT NULL
);

INSERT INTO dim_customer (customer_id, customer_name, gender, member_level) VALUES
(1, '张三', '男', '普通会员'),
(2, '李四', '女', '银牌会员'),
(3, '王五', '男', '黄金会员'),
(4, '赵六', '女', '黄金会员'),
(5, '钱七', '女', '普通会员');

CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    brand VARCHAR(50) NOT NULL
);

INSERT INTO dim_product (product_id, product_name, category, brand) VALUES
(1, 'iPhone 15', '手机', 'Apple'),
(2, 'Mate 60', '手机', 'Huawei'),
(3, 'ThinkPad X1', '电脑', 'Lenovo'),
(4, 'AirPods Pro', '耳机', 'Apple'),
(5, '小米手环', '智能穿戴', 'Xiaomi');

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL
);

INSERT INTO dim_date (date_id, full_date, year, quarter, month, day) VALUES
(1, '2024-01-01', 2024, 1, 1, 1),
(2, '2024-01-02', 2024, 1, 1, 2),
(3, '2024-02-01', 2024, 1, 2, 1),
(4, '2024-03-01', 2024, 1, 3, 1),
(5, '2024-04-01', 2024, 2, 4, 1);

CREATE TABLE fact_order (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    date_id INT NOT NULL,
    region_id INT NOT NULL,
    order_quantity INT NOT NULL,
    order_amount DECIMAL(10, 2) NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id)
);

INSERT INTO fact_order (
    order_id,
    customer_id,
    product_id,
    date_id,
    region_id,
    order_quantity,
    order_amount
) VALUES
(1, 1, 1, 1, 1, 1, 5999.00),
(2, 2, 2, 2, 2, 1, 5499.00),
(3, 3, 3, 3, 3, 1, 8999.00),
(4, 4, 4, 4, 1, 2, 1998.00),
(5, 5, 5, 5, 4, 3, 597.00),
(6, 3, 1, 5, 5, 1, 5999.00),
(7, 4, 2, 3, 2, 2, 10998.00),
(8, 2, 4, 1, 3, 1, 999.00);