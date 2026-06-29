#include <iostream>

int main() {
    std::cout << "system_name,vector_a,vector_b,dot_product,orthogonal_under_tolerance,residual_norm,orthonormality_error,warning\n";
    std::cout << "three_component_orthogonality_audit,3.000000;1.000000;2.000000,1.000000;-1.000000;-1.000000,0.000000,1,3.741657,0.000000,Orthogonality depends on geometry scaling units and tolerance.\n";
    return 0;
}
