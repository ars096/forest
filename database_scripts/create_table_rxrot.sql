# mysql

# create_rx_rotator_monitor_table.sql
# ----------------------------------
# Create Rx Rotator monitor table.
#

CREATE TABLE IF NOT EXISTS forest.rxrot_status(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       REAL_ANGLE FLOAT default NULL,
       REAL_VEL FLOAT default NULL,
       PROG_ANGLE FLOAT default NULL,
       COSMOS_ANGLE FLOAT default NULL,
       RESIDUAL FLOAT default NULL,
       TRACKING INT default NULL,
       SHUTDOWN_FLAG TINYINT default NULL,
       SOFTLIMIT0_FLAG TINYINT default NULL,
       SOFTLIMIT1_FLAG TINYINT default NULL,
       SOFTLIMIT2_FLAG TINYINT default NULL,
       COSMOS_FLAG TINYINT default NULL,
       PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS forest.rxrot_errors(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       ERROR VARCHAR(256) default NULL,
       PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS forest.rxrot_cosmos_log(
       id INT NOT NULL AUTO_INCREMENT,
       timestamp DATETIME NOT NULL,
       RECV_MSG VARCHAR(30) default NULL,
       SEND_MSG VARCHAR(85) default NULL,
       PRIMARY KEY (id)
);
