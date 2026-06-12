#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const double budget = 75.0;
    const int equity_floor = 1;

    int feasible_count = 0;
    int candidate_count = 0;
    double best_benefit = -1.0;
    int best[4] = {0, 0, 0, 0};

    printf("a_housing,b_health,c_transport,d_resilience,total_cost,total_benefit,feasible\n");

    for (int a = 0; a <= 8; ++a) {
        for (int b = 0; b <= 8; ++b) {
            for (int c = 0; c <= 8; ++c) {
                for (int d = 0; d <= 8; ++d) {
                    double total_cost = 7.0*a + 8.0*b + 5.0*c + 6.0*d;
                    double total_benefit = 11.0*a + 13.0*b + 8.0*c + 10.0*d;
                    int feasible = total_cost <= budget &&
                                   a >= equity_floor &&
                                   b >= equity_floor &&
                                   c >= equity_floor &&
                                   d >= equity_floor;

                    candidate_count++;
                    if (feasible) {
                        feasible_count++;
                        if (total_benefit > best_benefit) {
                            best_benefit = total_benefit;
                            best[0] = a;
                            best[1] = b;
                            best[2] = c;
                            best[3] = d;
                        }
                    }

                    printf("%d,%d,%d,%d,%.6f,%.6f,%d\n",
                           a, b, c, d, total_cost, total_benefit, feasible);
                }
            }
        }
    }

    fprintf(stderr,
            "c candidates=%d feasible=%d best_benefit=%.6f best_allocation=%d,%d,%d,%d\n",
            candidate_count, feasible_count, best_benefit, best[0], best[1], best[2], best[3]);
    return EXIT_SUCCESS;
}
