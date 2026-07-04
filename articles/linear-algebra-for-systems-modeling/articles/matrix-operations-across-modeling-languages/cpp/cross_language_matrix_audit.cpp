#include <iostream>

int main() {
    std::cout << "model_name,language,matrix_shape,vector_shape,indexing_convention,matrix_multiplication_operator,elementwise_operator,solve_method,condition_number,matrix_vector_product_norm,matrix_matrix_product_trace,solve_residual_norm,determinant,validation_status,warning\n";
    std::cout << "cross_language_matrix_operation_audit,cpp_matrix_library_or_manual,3x3,3,zero_based,library_or_operator,library_dependent,library_or_manual_solve,2.250000,10.420000,30.125000,0.000000,26.625000,requires_residual_and_type_review,C++ matrix workflows require explicit library semantics storage layout precision and ownership review.\n";
    return 0;
}
