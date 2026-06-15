DROP TABLE IF EXISTS inverse_model_assumption_registry;

CREATE TABLE inverse_model_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO inverse_model_assumption_registry VALUES
('domain_restriction','Domain restriction','The inverse is defined relative to a specified admissible domain.','Identifies the regime, branch, or feasible set under which recovery is meaningful.','Changing the domain can change or destroy the inverse.'),
('injectivity','Injectivity','Different admissible inputs must produce different outputs.','Supports uniqueness of recovered states or parameters.','If the forward model is many-to-one, inverse interpretation is ambiguous.'),
('local_invertibility','Local invertibility','A nonzero derivative or invertible Jacobian supports local inverse recovery.','Allows local reconstruction near an operating point.','Local invertibility does not imply global invertibility.'),
('conditioning','Conditioning','Inverse sensitivity depends on the reciprocal derivative or inverse Jacobian.','Shows whether recovered inputs are stable under output noise.','Ill-conditioned inverse maps can make precise recovery misleading.'),
('identifiability','Identifiability','Parameters or states must be recoverable from available outputs.','Connects inverse functions with calibration and diagnosis.','Similar outputs from different inputs weaken interpretive claims.');
