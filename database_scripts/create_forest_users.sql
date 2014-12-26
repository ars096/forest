# mysql

# create_forest_users.sql
# --------------------------
# Create users for forest project.
#

GRANT SELECT
      ON forest.* 
      TO forest_reader
      IDENTIFIED BY "forest";

GRANT SELECT,UPDATE,INSERT 
      ON forest.* 
      TO forest_writer
      IDENTIFIED BY "forestroot";


