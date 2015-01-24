# mysql

# create_switch_monitor_table.sql
# ----------------------------------
# Create IF switch monitor table.
#

CREATE TABLE IF NOT EXISTS forest.IF_switch(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       CH1 TINYINT default NULL,
       CH2 TINYINT default NULL,
       CH3 TINYINT default NULL,
       CH4 TINYINT default NULL,
       PRIMARY KEY (id)
);
