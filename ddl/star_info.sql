DROP TABLE IF EXISTS star_info;
CREATE TABLE star_info (
  const     VARCHAR(50),
  proper    VARCHAR(50),
  bayer     VARCHAR(50),
  flamsteed VARCHAR(50),
  gold      VARCHAR(50),
  variable  VARCHAR(50),
  hd        VARCHAR(50),
  hip       VARCHAR(50),
  vis_mag   VARCHAR(50),
  abs_mag   VARCHAR(50),
  dist      VARCHAR(50),
  sp_class  VARCHAR(50),
  summary   VARCHAR(4000)
);

\copy star_info from contellations_wiki_outputFinalwSummary.csv csv
