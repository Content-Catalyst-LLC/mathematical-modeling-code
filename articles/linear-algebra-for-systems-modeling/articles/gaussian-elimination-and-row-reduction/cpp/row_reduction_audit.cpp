#include <iostream>
int main() {
    std::cout << "system_name,equation_count,unknown_count,pivot_columns,coefficient_rank,augmented_rank,consistent,solution_behavior,tolerance,warning\n";
    std::cout << "three_constraint_resource_balance_system,3,3,0;1;2,3,3,1,unique solution,0.0000000001,Row reduction reveals algebraic structure but feasibility requires review.\n";
    return 0;
}
