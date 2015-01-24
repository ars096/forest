# mysql

# create_lo_sg_monitor_table.sql
# ----------------------------------
# Create LO SG monitor table.
#

CREATE TABLE IF NOT EXISTS forest.lo_sg(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       FREQ1 DOUBLE default NULL,
       POWER1 FLOAT default NULL,
       OUTPUT1 TINYINT default NULL,
       FREQ2 DOUBLE default NULL,
       POWER2 FLOAT default NULL,
       OUTPUT2 TINYINT default NULL,
       PRIMARY KEY (id)
);
