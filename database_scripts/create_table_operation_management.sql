# mysql

# create_operation_management_table.sql
# ----------------------------------
# Create operation management table.
#

CREATE TABLE IF NOT EXISTS forest.operation_log(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       flag VARCHAR(16) default NULL,
       method VARCHAR(64) default NULL,
       args VARCHAR(1024) default NULL,
       PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS forest.operation_console_log(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       msg VARCHAR(256) default NULL,
       PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS forest.operation_error_log(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       error VARCHAR(256) default NULL,
       PRIMARY KEY (id)
);


