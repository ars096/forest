# mysql

# create_spana_monitor_table.sql
# ----------------------------------
# Create spectrum analyzer monitor table.
#

CREATE TABLE IF NOT EXISTS forest.spana(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       SPANA1 TEXT default NULL,
       SPANA2 TEXT default NULL,
       SPANA3 TEXT default NULL,
       SPANA4 TEXT default NULL,
       PRIMARY KEY (id)
);
