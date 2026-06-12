#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

int mod_index(int value, int n) {
    int result = value % n;
    return result < 0 ? result + n : result;
}

int main(void) {
    const int n = 20;
    const int steps = 10;
    const double threshold = 0.35;
    bool adopted[20] = {false};

    adopted[0] = true;
    adopted[1] = true;
    adopted[2] = true;

    printf("step,adopted_count,adoption_share\n");

    for (int t = 0; t <= steps; ++t) {
        int adopted_count = 0;
        for (int i = 0; i < n; ++i) {
            if (adopted[i]) adopted_count++;
        }

        printf("%d,%d,%.6f\n", t, adopted_count, (double)adopted_count / (double)n);

        bool next[20];
        for (int i = 0; i < n; ++i) next[i] = adopted[i];

        for (int i = 0; i < n; ++i) {
            if (adopted[i]) continue;

            int local_count = 0;
            int local[4] = {
                mod_index(i - 2, n),
                mod_index(i - 1, n),
                mod_index(i + 1, n),
                mod_index(i + 2, n)
            };

            for (int j = 0; j < 4; ++j) {
                if (adopted[local[j]]) local_count++;
            }

            if ((double)local_count / 4.0 >= threshold) {
                next[i] = true;
            }
        }

        for (int i = 0; i < n; ++i) adopted[i] = next[i];
    }

    fprintf(stderr, "c abm_adoption_model complete\n");
    return EXIT_SUCCESS;
}
