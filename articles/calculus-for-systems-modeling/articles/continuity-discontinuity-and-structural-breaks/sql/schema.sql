DROP TABLE IF EXISTS continuity_concept_registry;
DROP TABLE IF EXISTS continuity_diagnostic_threshold;
DROP TABLE IF EXISTS structural_break_type;

CREATE TABLE continuity_concept_registry (
    concept_key TEXT PRIMARY KEY,
    concept_name TEXT NOT NULL,
    formal_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

CREATE TABLE continuity_diagnostic_threshold (
    threshold_key TEXT PRIMARY KEY,
    threshold_value REAL NOT NULL CHECK (threshold_value >= 0),
    interpretation TEXT NOT NULL
);

CREATE TABLE structural_break_type (
    break_key TEXT PRIMARY KEY,
    break_name TEXT NOT NULL,
    diagnostic_signal TEXT NOT NULL,
    modeling_warning TEXT NOT NULL
);

INSERT INTO continuity_concept_registry VALUES
('epsilon_delta_continuity','Epsilon-delta continuity','Defines local preservation of nearby values through input and output tolerances.','Supports local approximation, sensitivity, and derivative-based reasoning.','Requires a specified domain, codomain, and metric or topology.'),
('jump_discontinuity','Jump discontinuity','Occurs when one-sided limits exist but differ.','Represents thresholds, switches, interventions, or regime boundaries.','Derivative-based methods fail at the jump.'),
('structural_break','Structural break','Represents a change in the model relationship, not only output level.','Indicates that pre-break and post-break dynamics may require different models.','Can occur in slope, variance, parameters, governing equations, or mechanism.'),
('lipschitz_continuity','Lipschitz continuity','Bounds output differences by a constant multiple of input differences.','Supports stability, uniqueness, and error control in dynamic models.','May fail near singularities, thresholds, or unbounded derivatives.'),
('absolute_continuity','Absolute continuity','Allows recovery of a function from integration of its derivative almost everywhere.','Supports stock-flow interpretation and accumulated-change models.','Jump trajectories require alternative representations.');

INSERT INTO continuity_diagnostic_threshold VALUES
('jump_threshold',1.0,'Level change above this value is flagged for review.'),
('slope_threshold',0.5,'Slope change above this value is flagged for review.');

INSERT INTO structural_break_type VALUES
('level_break','Level break','Large one-step change in output.','May represent a jump, reporting artifact, shock, or intervention.'),
('slope_break','Slope break','Large change between left and right finite-difference slopes.','May preserve level continuity while changing mechanism.'),
('regime_break','Regime break','Change in level and slope or parameters.','Pre-break and post-break regions may require different models.');
