# mysql

# create_dewar_temp_monitor_table.sql
# ----------------------------------
# Create dewar temperature monitor table.
#

CREATE TABLE IF NOT EXISTS forest.dewar_temp(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       SENSOR1 VARCHAR(256) default NULL,
       K1 FLOAT default NULL,
       SU1 FLOAT default NULL,
       SENSOR2 VARCHAR(256) default NULL,
       K2 FLOAT default NULL,
       SU2 FLOAT default NULL,
       SENSOR3 VARCHAR(256) default NULL,
       K3 FLOAT default NULL,
       SU3 FLOAT default NULL,
       SENSOR4 VARCHAR(256) default NULL,
       K4 FLOAT default NULL,
       SU4 FLOAT default NULL,
       SENSOR5 VARCHAR(256) default NULL,
       K5 FLOAT default NULL,
       SU5 FLOAT default NULL,
       SENSOR6 VARCHAR(256) default NULL,
       K6 FLOAT default NULL,
       SU6 FLOAT default NULL,
       SENSOR7 VARCHAR(256) default NULL,
       K7 FLOAT default NULL,
       SU7 FLOAT default NULL,
       SENSOR8 VARCHAR(256) default NULL,
       K8 FLOAT default NULL,
       SU8 FLOAT default NULL,
       PRIMARY KEY (id)
);
