# mysql

# create_irr_sg_monitor_table.sql
# ----------------------------------
# Create IRR SG monitor table.
#

CREATE TABLE IF NOT EXISTS forest.lo_sg(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       FREQ DOUBLE default NULL,
       POWER FLOAT default NULL,
       OUTPUT TINYINT default NULL,
       PRIMARY KEY (id)
);
