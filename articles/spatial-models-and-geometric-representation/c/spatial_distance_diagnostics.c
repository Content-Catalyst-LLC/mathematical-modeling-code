#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *key;
    const char *kind;
    double x;
    double y;
    double value;
} Location;

double distance_between(Location a, Location b) {
    return sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
}

int main(void) {
    Location locations[] = {
        {"neighborhood_a", "demand", 0.0, 0.0, 1200},
        {"neighborhood_b", "demand", 2.0, 1.0, 900},
        {"neighborhood_c", "demand", 4.0, 2.5, 1400},
        {"neighborhood_d", "demand", 6.0, 1.5, 700},
        {"clinic_1", "service", 1.0, 0.5, 500},
        {"clinic_2", "service", 5.5, 2.0, 650},
        {"clinic_3", "service", 3.0, 4.0, 400}
    };

    const int count = (int)(sizeof(locations) / sizeof(locations[0]));

    printf("demand_location,nearest_service,nearest_distance,accessibility_score\n");

    for (int i = 0; i < count; ++i) {
        if (locations[i].kind[0] != 'd') continue;

        const char *nearest = "";
        double nearest_distance = 1.0e99;
        double accessibility = 0.0;

        for (int j = 0; j < count; ++j) {
            if (locations[j].kind[0] != 's') continue;
            double d = distance_between(locations[i], locations[j]);
            accessibility += locations[j].value / (1.0 + d);
            if (d < nearest_distance) {
                nearest_distance = d;
                nearest = locations[j].key;
            }
        }

        printf("%s,%s,%.6f,%.6f\n", locations[i].key, nearest, nearest_distance, accessibility);
    }

    fprintf(stderr, "c spatial_distance_diagnostics complete\n");
    return EXIT_SUCCESS;
}
