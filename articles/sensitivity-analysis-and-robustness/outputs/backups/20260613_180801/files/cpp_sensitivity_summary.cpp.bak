#include <cmath>
#include <iomanip>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct Parameter {
    std::string name;
    double baseline;
    double low;
    double high;
    std::string label;
};

double projection(double initial_stock, double growth_rate, double carrying_capacity, double extraction_rate, double shock_intensity) {
    double stock = initial_stock;
    for (int year = 0; year < 10; ++year) {
        const double growth = growth_rate * stock * (1.0 - stock / carrying_capacity);
        const double extraction = extraction_rate * stock;
        const double shock = shock_intensity * stock;
        stock = std::max(0.0, stock + growth - extraction - shock);
    }
    return stock;
}

int main() {
    std::vector<Parameter> params = {
        {"initial_stock", 80.0, 72.0, 88.0, "measurement"},
        {"growth_rate", 0.08, 0.04, 0.12, "parameter"},
        {"carrying_capacity", 120.0, 100.0, 140.0, "structural"},
        {"extraction_rate", 0.12, 0.08, 0.18, "policy"},
        {"shock_intensity", 0.03, 0.00, 0.08, "scenario"}
    };

    std::map<std::string, double> base;
    for (const auto& p : params) {
        base[p.name] = p.baseline;
    }

    std::cout << "parameter,low_output,baseline_output,high_output,range_width\n";
    const double base_output = projection(base["initial_stock"], base["growth_rate"], base["carrying_capacity"], base["extraction_rate"], base["shock_intensity"]);

    for (const auto& p : params) {
        std::map<std::string, double> low = base;
        std::map<std::string, double> high = base;
        low[p.name] = p.low;
        high[p.name] = p.high;

        const double low_output = projection(low["initial_stock"], low["growth_rate"], low["carrying_capacity"], low["extraction_rate"], low["shock_intensity"]);
        const double high_output = projection(high["initial_stock"], high["growth_rate"], high["carrying_capacity"], high["extraction_rate"], high["shock_intensity"]);
        const double width = std::abs(high_output - low_output);

        std::cout << std::fixed << std::setprecision(6)
                  << p.name << ","
                  << low_output << ","
                  << base_output << ","
                  << high_output << ","
                  << width << "\n";
    }

    return 0;
}
