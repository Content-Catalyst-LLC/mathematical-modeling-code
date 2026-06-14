#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    double width_m;
    double height_m;
    double span_m;
    double load_n;
    double allowable_stress_pa;
    double density;
} BeamDesign;

typedef struct {
    double stress;
    double margin;
    double safety_factor;
    double mass;
} Evaluation;

Evaluation evaluate(BeamDesign design) {
    double moment = design.load_n * design.span_m / 4.0;
    double inertia = design.width_m * design.height_m * design.height_m * design.height_m / 12.0;
    double c_value = design.height_m / 2.0;
    double stress = moment * c_value / inertia;
    double margin = design.allowable_stress_pa - stress;
    double safety_factor = design.allowable_stress_pa / stress;
    double mass = design.width_m * design.height_m * design.span_m * design.density;

    Evaluation result = {stress, margin, safety_factor, mass};
    return result;
}

int main(void) {
    BeamDesign designs[] = {
        {"light_design", 0.08, 0.16, 3.0, 4200.0, 145000000.0, 7850.0},
        {"balanced_design", 0.10, 0.18, 3.0, 4200.0, 145000000.0, 7850.0},
        {"stiff_design", 0.12, 0.22, 3.0, 4200.0, 145000000.0, 7850.0},
        {"overloaded_case", 0.10, 0.18, 3.0, 7000.0, 145000000.0, 7850.0}
    };

    printf("key,max_stress_pa,stress_margin_pa,safety_factor,estimated_mass_kg,passes_stress_constraint\n");

    for (int i = 0; i < 4; ++i) {
        Evaluation eval = evaluate(designs[i]);
        const char *passes = eval.stress <= designs[i].allowable_stress_pa ? "true" : "false";
        printf("%s,%.6f,%.6f,%.6f,%.6f,%s\n",
               designs[i].key,
               eval.stress,
               eval.margin,
               eval.safety_factor,
               eval.mass,
               passes);
    }

    fprintf(stderr, "engineering_design_summary complete\n");
    return EXIT_SUCCESS;
}
