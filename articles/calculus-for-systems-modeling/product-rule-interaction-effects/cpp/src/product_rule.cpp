#include <iostream>

int main() {
    double a = 120.0, b = 1.5, da = 4.0, db = 0.03;
    double ca = da * b;
    double cb = a * db;
    std::cout << "contribution_from_a=" << ca << "\n";
    std::cout << "contribution_from_b=" << cb << "\n";
    std::cout << "total_derivative=" << ca + cb << "\n";
}
