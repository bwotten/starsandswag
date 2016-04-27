DROP TABLE IF EXISTS const_names;
CREATE TABLE const_names (
  abb  VARCHAR(5),
  name VARCHAR(50),
  summary VARCHAR(256)
);

\copy const_names from constellations_wiki_output.csv csv
