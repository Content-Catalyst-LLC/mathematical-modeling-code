#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct BeamDesign {
    std::string key;
    double width_m;
    double height_m;
    double span_m;
    double load_n;
    double allowable_stress_pa;
    double density;
};

struct Evaluation {
    double stress;
    double margin;
    double safety_factor;
    double mass;
};

Evaluation evaluate(const BeamDesign& design) {
    const double moment = design.load_n * design.span_m / 4.0;
    const double inertia = design.width_m * design.height_m * design.height_m * design.height_m / 12.0;
    const double c_value = design.height_m / 2.0;
    const double stress = moment * c_value / inertia;
    const double margin = design.allowable_stress_pa - stress;
    const double safety_factor = design.allowable_stress_pa / stress;
    const double mass = design.width_m * design.height_m * design.span_m * design.density;
    return {stress, margin, safety_factor, mass};
}

int main() {
    std::vector<BeamDesign> designs = {
        {"light_design", 0.08, 0.16, 3.0, 4200.0, 145000000.0, 7850.0},
        {"balanced_design", 0.10, 0.18, 3.0, 4200.0, 145000000.0, 7850.0},
        {"stiff_design", 0.12, 0.22, 3.0, 4200.0, 145000000.0, 7850.0},
        {"overloaded_case", 0.10, 0.18, 3.0, 7000.0, 145000000.0, 7850.0}
    };

    std::cout << "key,max_stress_pa,stress_margin_pa,safety_factor,estimated_mass_kg,passes_stress_constraint\n";
    for (const auto& design : designs) {
        const Evaluation eval = evaluate(design);
        const bool passes = eval.stress <= design.allowable_stress_pa;
        std::cout << std::fixed << std::setprecision(6)
                  << design.key << "," << eval.stress << "," << eval.margin << ","
                  << eval.safety_factor << "," << eval.mass << ","
                  << (passes ? "true" : "false") << "\n";
    }

    return 0;
}
