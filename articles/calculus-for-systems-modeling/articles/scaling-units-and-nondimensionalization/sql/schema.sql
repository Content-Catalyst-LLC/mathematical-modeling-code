DROP TABLE IF EXISTS scaling_governance_registry;
DROP TABLE IF EXISTS scaling_unit_records;

CREATE TABLE scaling_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO scaling_governance_registry VALUES
('unit_record','Unit record','Documents units, dimensions, conversion rules, and source notes.','Keeps model quantities interpretable and comparable.','A numerical value without a unit may be ambiguous or misleading.'),
('reference_scale','Reference scale','Defines the characteristic value used to normalize a quantity.','Turns raw magnitudes into comparable ratios.','Changing the reference scale changes dimensionless interpretation.'),
('dimensionless_variable','Dimensionless variable','Expresses a quantity as a ratio to a reference scale.','Supports comparison across systems with different units or sizes.','Dimensionless form still depends on documented scale choices.'),
('dimensionless_group','Dimensionless group','Combines variables and parameters so units cancel.','Reveals process ratios, regimes, and similarity classes.','Dimensionless groups require correct variable selection and interpretation.'),
('unit_conversion','Unit conversion','Transforms values across compatible unit systems.','Prevents hidden mismatches in time, length, mass, stock, or rate units.','Conversion rules should be explicit and reproducible.'),
('claim_boundary','Claim boundary','Defines how scaled or dimensionless results may be interpreted.','Prevents overclaiming from elegant mathematical form.','Scaling improves comparability but does not prove empirical validity.');

CREATE TABLE scaling_unit_records (
    record_id TEXT PRIMARY KEY,
    record_type TEXT NOT NULL,
    quantity_name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO scaling_unit_records VALUES
('unit_population_stock','unit_record','population_stock',40.0,'state units','synthetic teaching value','synthetic value; do not treat as empirical measurement');
INSERT INTO scaling_unit_records VALUES
('unit_carrying_capacity','unit_record','carrying_capacity',100.0,'state units','synthetic teaching capacity','capacity scale controls normalized interpretation');
INSERT INTO scaling_unit_records VALUES
('scale_stock','scale_record','stock_scale',100.0,'state units','carrying capacity used to normalize population stock','changing the capacity scale changes dimensionless stock');
INSERT INTO scaling_unit_records VALUES
('nondim_stock','nondimensional_record','scaled_stock',0.4,'dimensionless','population stock as fraction of carrying capacity','dimensionless form depends on documented scale choices');
