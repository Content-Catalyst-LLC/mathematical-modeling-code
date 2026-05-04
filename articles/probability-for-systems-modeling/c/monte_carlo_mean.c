#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const int n = 10000;
    unsigned int seed = 42;
    double total = 0.0;

    srand(seed);

    for (int i = 0; i < n; i++) {
        double exposure = 0.2 + 0.8 * ((double) rand() / RAND_MAX);
        double vulnerability = (double) rand() / RAND_MAX;
        double loss = exposure * vulnerability;
        total += loss;
    }

    printf("Monte Carlo mean loss estimate: %.8f\n", total / n);

    return 0;
}
