# mysql

# create_forest_users.sql
# --------------------------
# Create users for forest project.
#

GRANT SELECT
      ON forest.* 
      TO forest_reader
      IDENTIFIED "forest";

GRANT SELECT,UPDATE,INSERT 
      ON forest.* 
      TO forest_writer
      IDENTIFIED "forestroot";


