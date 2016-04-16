DROP TABLE IF EXISTS con_trans;
CREATE TABLE con_trans (
  name   VARCHAR(5),
  trans  VARCHAR(100)
);

\copy con_trans from con.csv csv
