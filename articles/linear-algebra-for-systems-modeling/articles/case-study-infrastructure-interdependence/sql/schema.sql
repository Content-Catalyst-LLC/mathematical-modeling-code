CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('case-study-infrastructure-interdependence', 'Case Study: Infrastructure Interdependence', 'planned', 'A worked example of connected infrastructure systems and vulnerability.');
