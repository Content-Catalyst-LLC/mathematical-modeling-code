-- Spatial models and geometric representation governance schema.

DROP TABLE IF EXISTS spatial_component_guide;
DROP TABLE IF EXISTS spatial_location;
DROP TABLE IF EXISTS spatial_model_register;
DROP TABLE IF EXISTS spatial_component_type;

CREATE TABLE spatial_component_type (
    component_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE spatial_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    component_type TEXT NOT NULL,
    geometry_or_structure TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (component_type) REFERENCES spatial_component_type(component_type)
);

CREATE TABLE spatial_location (
    location_key TEXT PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ('demand', 'service')),
    x REAL NOT NULL,
    y REAL NOT NULL,
    value REAL NOT NULL CHECK (value >= 0)
);

CREATE TABLE spatial_component_guide (
    component_type TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO spatial_component_type VALUES
('geometry','Spatial object representation.','Representation does not match model purpose.'),
('coordinate_system','Reference frame and units.','Units or projection are undocumented.'),
('distance_metric','How separation is measured.','Distance metric does not match movement or exposure.'),
('accessibility_metric','How access is scored.','Metric hides capacity, barriers, or values.'),
('neighborhood_rule','Which locations affect each other.','Neighborhoods are arbitrary.'),
('spatial_field','Value over space.','Interpolation uncertainty is hidden.'),
('validation_diagnostic','Credibility check.','Scale, boundary, and distance sensitivity are not tested.'),
('network_boundary','Included spatial extent.','Relevant context is excluded.');

INSERT INTO spatial_model_register(record_key, component_type, geometry_or_structure, interpretation, review_question, status) VALUES
('point_geometry','geometry','p=(x,y)','Facilities and observations are represented as point coordinates','Does point geometry oversimplify area shape or access?','review'),
('euclidean_distance','distance_metric','sqrt((x_i-x_j)^2+(y_i-y_j)^2)','Straight-line distance is used as a transparent baseline','Should network distance or travel time replace straight-line distance?','review'),
('service_access','accessibility_metric','capacity/(1+distance)','Service capacity is discounted by distance','Does the accessibility metric match the decision context?','review'),
('spatial_uncertainty','validation_diagnostic','distance_and_boundary_sensitivity','Spatial results require sensitivity checks','Are conclusions robust to distance and scale assumptions?','active'),
('coordinate_units','coordinate_system','planar_model_units','Coordinates are interpreted in shared planar units','Are units and reference frames documented?','review'),
('boundary_definition','network_boundary','study_area_extent','The model states which area is included','What relevant context is excluded?','review');

INSERT INTO spatial_location VALUES
('neighborhood_a','demand',0.0,0.0,1200),
('neighborhood_b','demand',2.0,1.0,900),
('neighborhood_c','demand',4.0,2.5,1400),
('neighborhood_d','demand',6.0,1.5,700),
('clinic_1','service',1.0,0.5,500),
('clinic_2','service',5.5,2.0,650),
('clinic_3','service',3.0,4.0,400);

INSERT INTO spatial_component_guide VALUES
('geometry','Spatial object representation','point line polygon grid surface','Does the geometry match the purpose?'),
('coordinate_system','Reference frame and units','planar meters or projected CRS','Are units and projection documented?'),
('distance_metric','How separation is measured','Euclidean distance','Does distance match movement or exposure?'),
('accessibility_metric','How access is scored','capacity discounted by distance','Does the metric support the decision?'),
('neighborhood_rule','Which locations affect each other','distance band or adjacency','Is the neighborhood justified?'),
('spatial_field','Value over space','risk surface or elevation','Is interpolation uncertainty represented?'),
('validation_diagnostic','Credibility check','boundary sensitivity','Are conclusions robust?');
