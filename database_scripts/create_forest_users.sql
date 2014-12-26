# mysql

# create_forest_users.sql
# --------------------------
# Create users for forest project.
#

CREATE USER forest_reader;
CREATE USER forest_writer;

GRANT SELECT ON forest.* TO forest_reader;
GRANT SELECT,UPDATE,INSERT ON forest.* TO forest_writer;


