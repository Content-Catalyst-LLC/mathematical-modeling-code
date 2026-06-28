#include <iostream>

int main() {
    int equation_count = 3;
    int unknown_count = 3;
    int coefficient_rank = 3;
    int augmented_rank = 3;
    bool consistent = true;

    std::cout << "system_name,equation_count,unknown_count,coefficient_rank,augmented_rank,consistent,solution_behavior,warning\n";
    std::cout << "three_constraint_resource_balance_system,"
              << equation_count << "," << unknown_count << ","
              << coefficient_rank << "," << augmented_rank << ","
              << consistent
              << ",unique solution,Algebraic consistency does not guarantee practical feasibility.\n";
    return 0;
}
