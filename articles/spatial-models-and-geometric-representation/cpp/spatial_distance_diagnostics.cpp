#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

struct Location {
    std::string key;
    std::string kind;
    double x;
    double y;
    double value;
};

double distance(const Location& a, const Location& b) {
    return std::sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
}

int main() {
    const std::vector<Location> locations = {
        {"neighborhood_a", "demand", 0.0, 0.0, 1200},
        {"neighborhood_b", "demand", 2.0, 1.0, 900},
        {"neighborhood_c", "demand", 4.0, 2.5, 1400},
        {"neighborhood_d", "demand", 6.0, 1.5, 700},
        {"clinic_1", "service", 1.0, 0.5, 500},
        {"clinic_2", "service", 5.5, 2.0, 650},
        {"clinic_3", "service", 3.0, 4.0, 400}
    };

    std::cout << "demand_location,nearest_service,nearest_distance,accessibility_score\n";

    for (const auto& demand : locations) {
        if (demand.kind != "demand") continue;

        std::string nearest;
        double nearest_distance = std::numeric_limits<double>::infinity();
        double accessibility = 0.0;

        for (const auto& service : locations) {
            if (service.kind != "service") continue;
            const double d = distance(demand, service);
            accessibility += service.value / (1.0 + d);
            if (d < nearest_distance) {
                nearest_distance = d;
                nearest = service.key;
            }
        }

        std::cout << demand.key << ","
                  << nearest << ","
                  << std::fixed << std::setprecision(6)
                  << nearest_distance << ","
                  << accessibility << "\n";
    }

    return 0;
}
