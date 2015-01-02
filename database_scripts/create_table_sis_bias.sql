# mysql

# create_sis_bias_monitor_table.sql
# ----------------------------------
# Create SIS bias monitor table.
#

CREATE TABLE IF NOT EXISTS forest.sis_bias(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       BIAS_V01 FLOAT default NULL,
       BIAS_I01 FLOAT default NULL,
       BIAS_V02 FLOAT default NULL,
       BIAS_I02 FLOAT default NULL,
       BIAS_V03 FLOAT default NULL,
       BIAS_I03 FLOAT default NULL,
       BIAS_V04 FLOAT default NULL,
       BIAS_I04 FLOAT default NULL,
       BIAS_V05 FLOAT default NULL,
       BIAS_I05 FLOAT default NULL,
       BIAS_V06 FLOAT default NULL,
       BIAS_I06 FLOAT default NULL,
       BIAS_V07 FLOAT default NULL,
       BIAS_I07 FLOAT default NULL,
       BIAS_V08 FLOAT default NULL,
       BIAS_I08 FLOAT default NULL,
       BIAS_V09 FLOAT default NULL,
       BIAS_I09 FLOAT default NULL,
       BIAS_V10 FLOAT default NULL,
       BIAS_I10 FLOAT default NULL,
       BIAS_V11 FLOAT default NULL,
       BIAS_I11 FLOAT default NULL,
       BIAS_V12 FLOAT default NULL,
       BIAS_I12 FLOAT default NULL,
       BIAS_V13 FLOAT default NULL,
       BIAS_I13 FLOAT default NULL,
       BIAS_V14 FLOAT default NULL,
       BIAS_I14 FLOAT default NULL,
       BIAS_V15 FLOAT default NULL,
       BIAS_I15 FLOAT default NULL,
       BIAS_V16 FLOAT default NULL,
       BIAS_I16 FLOAT default NULL,
       PRIMARY KEY (id)
);
