# mysql

# create_slider_monitor_table.sql
# ----------------------------------
# Create sliding chopper monitor table.
#

CREATE TABLE IF NOT EXISTS forest.slider_status(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       POSITION VARCHAR(5) default NULL,
       COUNT INT default NULL, 
       PRIMARY KEY (id)
);
