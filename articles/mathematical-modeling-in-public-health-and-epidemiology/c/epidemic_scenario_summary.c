#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    const char *scenario_name;
    double population;
    double initial_infectious;
    double initial_recovered;
    double beta;
    double gamma;
    int days;
    double hospital_capacity;
    double hospitalization_rate;
} EpidemicScenario;

typedef struct {
    double r0_simple;
    double peak_infectious;
    double peak_hospital_demand;
    double capacity_margin;
    int capacity_breach;
} Evaluation;

Evaluation evaluate(EpidemicScenario scenario) {
    double susceptible = scenario.population - scenario.initial_infectious - scenario.initial_recovered;
    double infectious = scenario.initial_infectious;
    double recovered = scenario.initial_recovered;
    double peak_infectious = infectious;
    double peak_hospital_demand = infectious * scenario.hospitalization_rate;

    for (int day = 0; day < scenario.days; ++day) {
        double new_infections = scenario.beta * susceptible * infectious / scenario.population;
        double new_recoveries = scenario.gamma * infectious;

        susceptible -= new_infections;
        if (susceptible < 0.0) {
            susceptible = 0.0;
        }

        infectious = infectious + new_infections - new_recoveries;
        if (infectious < 0.0) {
            infectious = 0.0;
        }

        recovered += new_recoveries;
        if (recovered > scenario.population) {
            recovered = scenario.population;
        }

        if (infectious > peak_infectious) {
            peak_infectious = infectious;
        }

        double hospital_demand = infectious * scenario.hospitalization_rate;
        if (hospital_demand > peak_hospital_demand) {
            peak_hospital_demand = hospital_demand;
        }
    }

    Evaluation result = {
        scenario.beta / scenario.gamma,
        peak_infectious,
        peak_hospital_demand,
        scenario.hospital_capacity - peak_hospital_demand,
        peak_hospital_demand > scenario.hospital_capacity
    };
    return result;
}

int main(void) {
    EpidemicScenario scenarios[] = {
        {"baseline", "Baseline transmission", 100000.0, 120.0, 4000.0, 0.32, 0.12, 120, 850.0, 0.045},
        {"moderate_intervention", "Moderate intervention", 100000.0, 120.0, 4000.0, 0.24, 0.12, 120, 850.0, 0.045},
        {"strong_intervention", "Strong intervention", 100000.0, 120.0, 4000.0, 0.18, 0.12, 120, 850.0, 0.045},
        {"vaccination_plus_intervention", "Vaccination plus intervention", 100000.0, 120.0, 22000.0, 0.20, 0.12, 120, 850.0, 0.030}
    };

    printf("key,r0_simple,peak_infectious,peak_hospital_demand,capacity_margin,capacity_breach\n");

    for (int i = 0; i < 4; ++i) {
        Evaluation eval = evaluate(scenarios[i]);
        printf("%s,%.6f,%.6f,%.6f,%.6f,%s\n",
               scenarios[i].key,
               eval.r0_simple,
               eval.peak_infectious,
               eval.peak_hospital_demand,
               eval.capacity_margin,
               eval.capacity_breach ? "true" : "false");
    }

    fprintf(stderr, "epidemic_scenario_summary complete\n");
    return EXIT_SUCCESS;
}
