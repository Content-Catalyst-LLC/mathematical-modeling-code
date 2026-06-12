#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *name;
    double budget;
    double cost_a;
    double cost_b;
    double benefit_a;
    double benefit_b;
    double allocation_a;
    double allocation_b;
    double capacity_a;
    double capacity_b;
} Scenario;

int main(void) {
    Scenario scenarios[] = {
        {"c_balanced_feasible", 100.0, 4.0, 5.0, 8.0, 11.0, 10.0, 8.0, 20.0, 15.0},
        {"c_capacity_stress", 120.0, 4.0, 5.0, 8.0, 11.0, 25.0, 5.0, 20.0, 15.0}
    };

    printf("scenario,total_cost,total_benefit,benefit_per_cost,budget_slack,capacity_slack_a,capacity_slack_b,feasible\n");

    for (int i = 0; i < 2; ++i) {
        Scenario s = scenarios[i];

        double total_cost = s.cost_a * s.allocation_a + s.cost_b * s.allocation_b;
        double total_benefit = s.benefit_a * s.allocation_a + s.benefit_b * s.allocation_b;
        double benefit_per_cost = total_cost > 0.0 ? total_benefit / total_cost : 0.0;
        double budget_slack = s.budget - total_cost;
        double capacity_slack_a = s.capacity_a - s.allocation_a;
        double capacity_slack_b = s.capacity_b - s.allocation_b;
        int feasible = budget_slack >= 0.0 && capacity_slack_a >= 0.0 && capacity_slack_b >= 0.0;

        printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d\n",
               s.name, total_cost, total_benefit, benefit_per_cost, budget_slack, capacity_slack_a, capacity_slack_b, feasible);
    }

    fprintf(stderr, "c static allocation workflow complete\n");
    return EXIT_SUCCESS;
}
