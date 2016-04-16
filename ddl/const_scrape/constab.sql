DROP TABLE IF EXISTS const_names;
CREATE TABLE const_names (
  abb  VARCHAR(5),
  full_name VARCHAR(50)
);

\copy const_names from const_names.csv csv
