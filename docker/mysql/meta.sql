SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `shopkeeper_meta`
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE `shopkeeper_meta`;

CREATE TABLE IF NOT EXISTS `table_info`
(
    `id` VARCHAR(64) PRIMARY KEY,
    `name` VARCHAR(128) NOT NULL,
    `role` VARCHAR(32) NOT NULL,
    `description` TEXT
);

CREATE TABLE IF NOT EXISTS `column_info`
(
    `id` VARCHAR(64) PRIMARY KEY,
    `name` VARCHAR(128) NOT NULL,
    `type` VARCHAR(64) NOT NULL,
    `role` VARCHAR(32) NOT NULL,
    `examples` JSON,
    `description` TEXT,
    `alias` JSON,
    `table_id` VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS `metric_info`
(
    `id` VARCHAR(64) PRIMARY KEY,
    `name` VARCHAR(128) NOT NULL,
    `description` TEXT,
    `relevant_columns` JSON,
    `alias` JSON
);

CREATE TABLE IF NOT EXISTS `column_metric`
(
    `column_id` VARCHAR(64) NOT NULL,
    `metric_id` VARCHAR(64) NOT NULL,
    PRIMARY KEY (`column_id`, `metric_id`)
);

INSERT INTO table_info (id, name, role, description)
VALUES
    ('table_fact_order', 'fact_order', 'fact', 'Order fact table'),
    ('table_dim_region', 'dim_region', 'dim', 'Region dimension table'),
    ('table_dim_customer', 'dim_customer', 'dim', 'Customer dimension table'),
    ('table_dim_product', 'dim_product', 'dim', 'Product dimension table'),
    ('table_dim_date', 'dim_date', 'dim', 'Date dimension table')
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    role = VALUES(role),
    description = VALUES(description);

INSERT INTO column_info
(
    id,
    name,
    type,
    role,
    examples,
    description,
    alias,
    table_id
)
VALUES
    (
        'column_fact_order_order_id',
        'order_id',
        'INT',
        'primary_key',
        JSON_ARRAY(10001, 10002),
        'Unique identifier of an order',
        JSON_ARRAY('order id', 'order number'),
        'table_fact_order'
    ),
    (
        'column_fact_order_customer_id',
        'customer_id',
        'INT',
        'foreign_key',
        JSON_ARRAY(1, 2),
        'Identifier of the customer who placed the order',
        JSON_ARRAY('customer id', 'buyer id'),
        'table_fact_order'
    ),
    (
        'column_fact_order_product_id',
        'product_id',
        'INT',
        'foreign_key',
        JSON_ARRAY(1, 2),
        'Identifier of the purchased product',
        JSON_ARRAY('product id', 'item id'),
        'table_fact_order'
    ),
    (
        'column_fact_order_date_id',
        'date_id',
        'INT',
        'foreign_key',
        JSON_ARRAY(20240101, 20240102),
        'Identifier of the order date',
        JSON_ARRAY('date id', 'order date id'),
        'table_fact_order'
    ),
    (
        'column_fact_order_region_id',
        'region_id',
        'INT',
        'foreign_key',
        JSON_ARRAY(1, 2),
        'Identifier of the order region',
        JSON_ARRAY('region id', 'area id'),
        'table_fact_order'
    ),
    (
        'column_fact_order_order_quantity',
        'order_quantity',
        'INT',
        'measure',
        JSON_ARRAY(1, 2, 3),
        'Number of product units purchased in the order',
        JSON_ARRAY('sales quantity', 'purchase quantity', 'units sold'),
        'table_fact_order'
    ),
    (
        'column_fact_order_order_amount',
        'order_amount',
        'DECIMAL(12,2)',
        'measure',
        JSON_ARRAY(1999.00, 5999.00),
        'Total monetary amount of the order',
        JSON_ARRAY('sales amount', 'revenue', 'order value'),
        'table_fact_order'
    )
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    type = VALUES(type),
    role = VALUES(role),
    examples = VALUES(examples),
    description = VALUES(description),
    alias = VALUES(alias),
    table_id = VALUES(table_id);

INSERT INTO column_info
(
    id,
    name,
    type,
    role,
    examples,
    description,
    alias,
    table_id
)
VALUES
    (
        'column_dim_region_region_id',
        'region_id',
        'INT',
        'primary_key',
        JSON_ARRAY(1, 2),
        'Unique identifier of a region',
        JSON_ARRAY('region id', 'area id'),
        'table_dim_region'
    ),
    (
        'column_dim_region_province',
        'province',
        'VARCHAR(100)',
        'dimension',
        JSON_ARRAY('Jiangsu', 'Zhejiang'),
        'Province associated with the order region',
        JSON_ARRAY('province', 'state'),
        'table_dim_region'
    ),
    (
        'column_dim_region_region_name',
        'region_name',
        'VARCHAR(100)',
        'dimension',
        JSON_ARRAY('East China', 'South China'),
        'Business region used for geographic analysis',
        JSON_ARRAY('region', 'area', 'sales region'),
        'table_dim_region'
    ),
    (
        'column_dim_region_country',
        'country',
        'VARCHAR(100)',
        'dimension',
        JSON_ARRAY('China'),
        'Country associated with the region',
        JSON_ARRAY('country', 'nation'),
        'table_dim_region'
    ),
    (
        'column_dim_product_product_id',
        'product_id',
        'INT',
        'primary_key',
        JSON_ARRAY(1, 2),
        'Unique identifier of a product',
        JSON_ARRAY('product id', 'item id'),
        'table_dim_product'
    ),
    (
        'column_dim_product_product_name',
        'product_name',
        'VARCHAR(200)',
        'dimension',
        JSON_ARRAY('iPhone 15', 'Mate 60'),
        'Display name of the product',
        JSON_ARRAY('product name', 'item name'),
        'table_dim_product'
    ),
    (
        'column_dim_product_category',
        'category',
        'VARCHAR(100)',
        'dimension',
        JSON_ARRAY('Phone', 'Computer'),
        'Category assigned to the product',
        JSON_ARRAY('category', 'product category'),
        'table_dim_product'
    ),
    (
        'column_dim_product_brand',
        'brand',
        'VARCHAR(100)',
        'dimension',
        JSON_ARRAY('Apple', 'Huawei'),
        'Brand associated with the product',
        JSON_ARRAY('brand', 'manufacturer'),
        'table_dim_product'
    )
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    type = VALUES(type),
    role = VALUES(role),
    examples = VALUES(examples),
    description = VALUES(description),
    alias = VALUES(alias),
    table_id = VALUES(table_id);

INSERT INTO column_info
(
    id,
    name,
    type,
    role,
    examples,
    description,
    alias,
    table_id
)
VALUES
    (
        'column_dim_customer_customer_id',
        'customer_id',
        'INT',
        'primary_key',
        JSON_ARRAY(1, 2),
        'Unique identifier of a customer',
        JSON_ARRAY('customer id', 'buyer id'),
        'table_dim_customer'
    ),
    (
        'column_dim_customer_customer_name',
        'customer_name',
        'VARCHAR(100)',
        'dimension',
        JSON_ARRAY('Customer A', 'Customer B'),
        'Display name of the customer',
        JSON_ARRAY('customer name', 'buyer name'),
        'table_dim_customer'
    ),
    (
        'column_dim_customer_gender',
        'gender',
        'VARCHAR(20)',
        'dimension',
        JSON_ARRAY('Male', 'Female'),
        'Gender of the customer',
        JSON_ARRAY('gender', 'sex'),
        'table_dim_customer'
    ),
    (
        'column_dim_customer_member_level',
        'member_level',
        'VARCHAR(50)',
        'dimension',
        JSON_ARRAY('Standard', 'Silver', 'Gold'),
        'Membership level assigned to the customer',
        JSON_ARRAY('membership level', 'customer tier', 'member tier'),
        'table_dim_customer'
    ),
    (
        'column_dim_date_date_id',
        'date_id',
        'INT',
        'primary_key',
        JSON_ARRAY(20240101, 20240102),
        'Numeric identifier of a calendar date',
        JSON_ARRAY('date id', 'calendar id'),
        'table_dim_date'
    ),
    (
        'column_dim_date_full_date',
        'full_date',
        'DATE',
        'dimension',
        JSON_ARRAY('2024-01-01', '2024-01-02'),
        'Complete calendar date',
        JSON_ARRAY('full date', 'calendar date', 'order date'),
        'table_dim_date'
    ),
    (
        'column_dim_date_year',
        'year',
        'INT',
        'dimension',
        JSON_ARRAY(2024),
        'Calendar year',
        JSON_ARRAY('year', 'calendar year'),
        'table_dim_date'
    ),
    (
        'column_dim_date_quarter',
        'quarter',
        'INT',
        'dimension',
        JSON_ARRAY(1, 2, 3, 4),
        'Calendar quarter number',
        JSON_ARRAY('quarter', 'calendar quarter'),
        'table_dim_date'
    ),
    (
        'column_dim_date_month',
        'month',
        'INT',
        'dimension',
        JSON_ARRAY(1, 2, 3),
        'Calendar month number',
        JSON_ARRAY('month', 'calendar month'),
        'table_dim_date'
    ),
    (
        'column_dim_date_day',
        'day',
        'INT',
        'dimension',
        JSON_ARRAY(1, 2, 3),
        'Day number within the month',
        JSON_ARRAY('day', 'day of month'),
        'table_dim_date'
    )
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    type = VALUES(type),
    role = VALUES(role),
    examples = VALUES(examples),
    description = VALUES(description),
    alias = VALUES(alias),
    table_id = VALUES(table_id);

INSERT INTO metric_info
(
    id,
    name,
    description,
    relevant_columns,
    alias
)
VALUES
    (
        'metric_total_sales',
        'total_sales',
        'Sum of order amounts for the selected records',
        JSON_ARRAY('column_fact_order_order_amount'),
        JSON_ARRAY('sales amount', 'revenue', 'gross sales')
    ),
    (
        'metric_order_count',
        'order_count',
        'Count of orders for the selected records',
        JSON_ARRAY('column_fact_order_order_id'),
        JSON_ARRAY('number of orders', 'order volume', 'transaction count')
    ),
    (
        'metric_sales_quantity',
        'sales_quantity',
        'Sum of product units sold for the selected records',
        JSON_ARRAY('column_fact_order_order_quantity'),
        JSON_ARRAY('units sold', 'sales volume', 'purchase quantity')
    ),
    (
        'metric_average_order_value',
        'average_order_value',
        'Average monetary amount of an order',
        JSON_ARRAY(
            'column_fact_order_order_amount',
            'column_fact_order_order_id'
        ),
        JSON_ARRAY('average order value', 'average transaction value')
    )
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    description = VALUES(description),
    relevant_columns = VALUES(relevant_columns),
    alias = VALUES(alias);

INSERT IGNORE INTO column_metric (column_id, metric_id)
VALUES
    (
        'column_fact_order_order_amount',
        'metric_total_sales'
    ),
    (
        'column_fact_order_order_id',
        'metric_order_count'
    ),
    (
        'column_fact_order_order_quantity',
        'metric_sales_quantity'
    ),
    (
        'column_fact_order_order_amount',
        'metric_average_order_value'
    ),
    (
        'column_fact_order_order_id',
        'metric_average_order_value'
    );