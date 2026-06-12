#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>

struct Edge {
    std::string source;
    std::string target;
    double weight;
};

int main() {
    const std::vector<Edge> edges = {
        {"power_substation", "hospital", 0.95},
        {"power_substation", "water_treatment", 0.90},
        {"communications_hub", "hospital", 0.70},
        {"fuel_depot", "power_substation", 0.60},
        {"transport_hub", "hospital", 0.50},
        {"transport_hub", "fuel_depot", 0.65},
        {"water_treatment", "hospital", 0.80},
        {"emergency_depot", "hospital", 0.75},
        {"communications_hub", "emergency_depot", 0.55},
        {"power_substation", "communications_hub", 0.85}
    };

    std::set<std::string> nodes;
    std::map<std::string, int> in_degree;
    std::map<std::string, int> out_degree;
    std::map<std::string, double> weighted_out;

    for (const auto& edge : edges) {
        nodes.insert(edge.source);
        nodes.insert(edge.target);
        out_degree[edge.source] += 1;
        in_degree[edge.target] += 1;
        weighted_out[edge.source] += edge.weight;
    }

    std::cout << "cpp node_count=" << nodes.size() << " edge_count=" << edges.size() << "\n";

    for (const auto& node : nodes) {
        std::cout << std::fixed << std::setprecision(2)
                  << node
                  << " in_degree=" << in_degree[node]
                  << " out_degree=" << out_degree[node]
                  << " weighted_out=" << weighted_out[node]
                  << "\n";
    }

    return 0;
}
