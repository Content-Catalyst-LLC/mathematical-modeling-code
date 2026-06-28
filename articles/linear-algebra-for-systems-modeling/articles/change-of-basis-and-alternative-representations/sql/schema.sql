CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('change-of-basis-and-alternative-representations', 'Change of Basis and Alternative Representations', 'planned', 'An article on how the same system can appear differently under different coordinate systems.');
