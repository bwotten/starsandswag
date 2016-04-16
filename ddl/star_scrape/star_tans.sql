DROP TABLE IF EXISTS Star_Trans;
CREATE TABLE Star_Trans (
  name   VARCHAR(100),
  translation VARCHAR(100)
);

\copy Star_Trans from star_trans.csv csv
