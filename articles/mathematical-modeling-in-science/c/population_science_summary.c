#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    double growth_rate;
    double carrying_capacity;
    double initial_population;
    int years;
} PopulationScenario;

double logistic_final(PopulationScenario scenario) {
    double population = scenario.initial_population;
    for (int year = 0; year < scenario.years; ++year) {
        population = population + scenario.growth_rate * population * (1.0 - population / scenario.carrying_capacity);
    }
    return population;
}

int main(void) {
    PopulationScenario scenarios[] = {
        {"baseline", 0.28, 500.0, 40.0, 20},
        {"lower_growth", 0.18, 500.0, 40.0, 20},
        {"higher_growth", 0.38, 500.0, 40.0, 20},
        {"lower_capacity", 0.28, 350.0, 40.0, 20},
        {"higher_capacity", 0.28, 700.0, 40.0, 20}
    };

    printf("key,growth_rate,carrying_capacity,initial_population,years,final_population,crosses_capacity_midpoint\n");

    for (int i = 0; i < 5; ++i) {
        double final_population = logistic_final(scenarios[i]);
        const char *crosses = final_population >= scenarios[i].carrying_capacity / 2.0 ? "true" : "false";
        printf("%s,%.3f,%.3f,%.3f,%d,%.6f,%s\n",
               scenarios[i].key,
               scenarios[i].growth_rate,
               scenarios[i].carrying_capacity,
               scenarios[i].initial_population,
               scenarios[i].years,
               final_population,
               crosses);
    }

    fprintf(stderr, "population_science_summary complete\n");
    return EXIT_SUCCESS;
}
