CREATE TABLE Stars (
  id     INTEGER,
  dist   NUMERIC,
  x      NUMERIC,
  y      NUMERIC,
  z      NUMERIC,
  ra     NUMERIC,
  dec    NUMERIC,
  mag    NUMERIC,
  con    varchar(5),
  lum    NUMERIC,
  proper VARCHAR(50)
);

\copy Stars from stars_trim.csv csv
