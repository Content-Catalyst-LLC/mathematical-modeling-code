#include <iostream>

int main() {
    int variable_count = 4;
    int equation_count = 3;
    int rank = 3;
    int nullity = variable_count - rank;

    std::cout << "system_name,variable_count,equation_count,rank,nullity,likely_solution_structure,warning\n";
    std::cout << "four_variable_three_constraint_system,"
              << variable_count << ","
              << equation_count << ","
              << rank << ","
              << nullity
              << ",Positive-dimensional solution space if consistent,Rank and nullity are mathematical diagnostics not proof of feasibility.\n";
    return 0;
}
