CREATE USER IF NOT EXISTS
    'shopkeeper_reader'@'%'
    IDENTIFIED BY 'local-reader-password';

ALTER USER
    'shopkeeper_reader'@'%'
    IDENTIFIED BY 'local-reader-password';

GRANT SELECT
    ON shopkeeper_dw.*
    TO 'shopkeeper_reader'@'%';

GRANT SELECT
    ON shopkeeper_meta.*
    TO 'shopkeeper_reader'@'%';

FLUSH PRIVILEGES;