#include <stdio.h>
#include <stdlib.h>

static double bounded_update(double raw_next, double capacity) {
    if (raw_next < 0.0) return 0.0;
    if (raw_next > capacity) return capacity;
    return raw_next;
}

int main(void) {
    double stock = 40.0;
    const double capacity = 60.0;
    const double inflow = 3.0;
    double demand = 7.0;
    const double loss_rate = 0.050;
    const double threshold = 25.0;
    const double demand_reduction = 1.0;
    const int periods = 60;
    double total_shortage = 0.0;
    int activations = 0;

    printf("period,stock,inflow,demand,losses,raw_next,constrained_next,shortage,logic_active\n");
    for (int period = 0; period <= periods; ++period) {
        double losses = loss_rate * stock;
        double raw_next = stock + inflow - demand - losses;
        double shortage = -raw_next;
        if (shortage < 0.0) shortage = 0.0;

        int logic_active = stock < threshold;
        if (logic_active) {
            activations += 1;
            demand -= demand_reduction;
            if (demand < 0.0) demand = 0.0;
        }

        double constrained_next = bounded_update(raw_next, capacity);

        printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d\n",
               period, stock, inflow, demand, losses, raw_next, constrained_next, shortage, logic_active);

        total_shortage += shortage;
        stock = constrained_next;
    }

    fprintf(stderr, "c final_stock=%.6f total_shortage=%.6f logic_activations=%d\n", stock, total_shortage, activations);
    return EXIT_SUCCESS;
}
