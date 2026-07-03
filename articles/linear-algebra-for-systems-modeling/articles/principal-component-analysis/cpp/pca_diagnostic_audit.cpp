#include <iostream>

int main() {
    std::cout << "model_name,observations,variables,preprocessing,retained_components,explained_variance_ratio,cumulative_explained_variance,relative_reconstruction_error,largest_loading_variable_pc1,largest_loading_variable_pc2,warning\n";
    std::cout << "synthetic_pca_diagnostic_audit,8,5,centered_and_standardized,2,0.946;0.044;0.007;0.002;0.001,0.990000,0.100000,transport_delay,water_demand,PCA requires data matrix preprocessing scaling retained-rank residual outlier and validation documentation.\n";
    return 0;
}
