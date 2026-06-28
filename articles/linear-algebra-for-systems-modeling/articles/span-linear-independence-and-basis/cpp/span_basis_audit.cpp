#include <array>
#include <cmath>
#include <iostream>

double determinant3x3(const std::array<std::array<double, 3>, 3>& m) {
    return m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1])
         - m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0])
         + m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]);
}

int main() {
    std::array<std::array<double, 3>, 3> matrix {{
        {{1.0, 0.0, 0.5}},
        {{0.0, 1.0, 0.5}},
        {{0.0, 0.0, 1.0}}
    }};

    int ambient_dimension = 3;
    int vector_count = 3;
    double det = determinant3x3(matrix);
    int rank = std::abs(det) > 1e-10 ? 3 : 2;
    bool spans = rank == ambient_dimension;
    bool independent = rank == vector_count;
    bool basis = spans && independent;

    std::cout << "vector_set_name,ambient_dimension,vector_count,rank,spans_ambient_space,linearly_independent,is_basis_for_ambient_space,warning\n";
    std::cout << "candidate_system_basis,3,3," << rank << "," << spans << "," << independent << "," << basis
              << ",A mathematical basis claim does not prove real-world adequacy.\n";
    return 0;
}
