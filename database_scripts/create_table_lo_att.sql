# mysql

# create_lo_att_monitor_table.sql
# ----------------------------------
# Create LO Att. bias monitor table.
#

CREATE TABLE IF NOT EXISTS forest.lo_att(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       BIAS_V01 FLOAT default NULL,
       BIAS_V02 FLOAT default NULL,
       BIAS_V03 FLOAT default NULL,
       BIAS_V04 FLOAT default NULL,
       BIAS_V05 FLOAT default NULL,
       BIAS_V06 FLOAT default NULL,
       BIAS_V07 FLOAT default NULL,
       BIAS_V08 FLOAT default NULL,
       BIAS_V09 FLOAT default NULL,
       PRIMARY KEY (id)
);
