DROP TABLE IF EXISTS change_of_basis_assumption_registry;
DROP TABLE IF EXISTS change_of_basis_audit_cases;

CREATE TABLE change_of_basis_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO change_of_basis_assumption_registry VALUES
('basis_vectors','Basis vectors','A linearly independent spanning set for the vector space.','Defines the coordinate language used to describe system states.','Basis directions should be meaningful or explicitly justified.'),
('basis_matrix','Basis matrix','A matrix whose columns are basis vectors.','Translates alternative coordinates into standard coordinates.','The matrix must be full rank for coordinates to be unique.'),
('coordinate_recovery','Coordinate recovery','Solves for coefficients in the chosen basis.','Finds how much of each basis direction contributes to a state.','Near-dependent bases can make recovered coordinates unstable.'),
('similarity_transformation','Similarity transformation','Represents the same transformation in a new basis.','Changes the matrix representation while preserving underlying structure.','Individual entries may change and should not be compared naively.'),
('invariant_structure','Invariant structure','Properties preserved under basis change.','Separates system behavior from coordinate artifacts.','Modelers should distinguish invariant claims from representation-specific claims.'),
('conditioning','Conditioning','Sensitivity of coordinate conversion to perturbation.','Shows whether the chosen basis is numerically stable.','Large condition numbers require caution before interpretation or decision use.');

CREATE TABLE change_of_basis_audit_cases (
    system_name TEXT NOT NULL,
    basis_shape TEXT NOT NULL,
    basis_rank INTEGER NOT NULL,
    basis_determinant REAL NOT NULL,
    original_vector TEXT NOT NULL,
    basis_coordinates TEXT NOT NULL,
    reconstructed_vector TEXT NOT NULL,
    reconstruction_error REAL NOT NULL,
    transformed_matrix TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO change_of_basis_audit_cases VALUES
('two_mode_representation_audit','2x2',2,3.0,'5.000000,4.000000','2.000000,1.500000','5.500000,5.000000',0.0,'1.133333,0.033333;0.333333,0.966667','Changing basis requires basis meaning units scaling conditioning and translation back to system terms.');
