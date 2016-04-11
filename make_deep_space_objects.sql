DROP TABLE IF EXISTS DSO;
CREATE TABLE DSO (
   id INTEGER,
   type varchar(15),
   ra NUMERIC,
   dec NUMERIC,
   mag NUMERIC,
   name (50),
   const varchar(5)
);

\copy DSO from dso_trimmed.csv csv
