#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { const char *name; double initial_state; double rate; double capacity; double time_horizon; } Scenario;

const char *validate_domain(Scenario s) {
    if (s.initial_state < 0.0) return "initial_state must be nonnegative";
    if (s.rate < 0.0) return "rate must be nonnegative";
    if (s.capacity <= 0.0) return "capacity must be positive";
    if (s.time_horizon < 0.0) return "time_horizon must be nonnegative";
    if (s.initial_state > s.capacity) return "initial_state exceeds capacity";
    return "";
}

double bounded_growth(Scenario s) {
    return s.capacity / (1.0 + ((s.capacity - s.initial_state) / s.initial_state) * exp(-s.rate * s.time_horizon));
}

int main(void) {
    Scenario scenarios[] = {
        {"baseline", 10.0, 0.20, 100.0, 20.0},
        {"near_capacity", 95.0, 0.20, 100.0, 20.0},
        {"invalid_negative_state", -5.0, 0.20, 100.0, 20.0},
        {"outside_capacity", 120.0, 0.20, 100.0, 20.0}
    };
    printf("scenario,status,value_or_issue\n");
    for (int i = 0; i < 4; ++i) {
        const char *issue = validate_domain(scenarios[i]);
        if (issue[0] != '\0') printf("%s,domain_review,%s\n", scenarios[i].name, issue);
        else printf("%s,ok,%.6f\n", scenarios[i].name, bounded_growth(scenarios[i]));
    }
    return EXIT_SUCCESS;
}
