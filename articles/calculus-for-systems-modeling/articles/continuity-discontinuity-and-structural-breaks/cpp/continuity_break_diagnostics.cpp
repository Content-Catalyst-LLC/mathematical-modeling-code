#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double piecewise_system(double x) {
    if (x < 5.0) {
        return 2.0 + 0.5 * x;
    }
    return 6.0 + 1.4 * (x - 5.0);
}

std::string classify(double level_jump, double slope_change) {
    if (level_jump > 1.0 && slope_change > 0.5) return "level_and_slope_break";
    if (level_jump > 1.0) return "possible_jump";
    if (slope_change > 0.5) return "possible_slope_break";
    return "ok";
}

int main() {
    std::vector<double> xs;
    std::vector<double> ys;

    for (int i = 0; i <= 40; ++i) {
        xs.push_back(0.25 * i);
        ys.push_back(piecewise_system(xs.back()));
    }

    std::cout << "x,y,left_slope,right_slope,slope_change,level_jump,flag\n";
    std::cout << std::fixed << std::setprecision(6);

    for (std::size_t i = 0; i < xs.size(); ++i) {
        if (i == 0 || i == xs.size() - 1) {
            std::cout << xs[i] << "," << ys[i] << ",,,,,ok\n";
        } else {
            double left_slope = (ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1]);
            double right_slope = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]);
            double slope_change = std::fabs(right_slope - left_slope);
            double level_jump = std::fabs(ys[i] - ys[i - 1]);
            std::cout << xs[i] << "," << ys[i] << ","
                      << left_slope << "," << right_slope << ","
                      << slope_change << "," << level_jump << ","
                      << classify(level_jump, slope_change) << "\n";
        }
    }

    return 0;
}
