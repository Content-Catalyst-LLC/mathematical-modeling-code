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
    const double feedback_strength = 0.20;
    const double loss_rate = 0.050;
    const int periods = 60;
    double total_shortage = 0.0;
    double total_overflow = 0.0;

    printf("period,stock,inflow,demand,losses,raw_next,next_stock,shortage,overflow\n");
    for (int period = 0; period <= periods; ++period) {
        double losses = loss_rate * stock;
        double raw_next = stock + inflow - demand - losses;
        double shortage = -raw_next;
        if (shortage < 0.0) shortage = 0.0;

        double overflow = raw_next - capacity;
        if (overflow < 0.0) overflow = 0.0;

        double next_stock = bounded_update(raw_next, capacity);

        printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
               period, stock, inflow, demand, losses, raw_next, next_stock, shortage, overflow);

        total_shortage += shortage;
        total_overflow += overflow;

        demand = demand - feedback_strength * shortage;
        if (demand < 0.0) demand = 0.0;

        stock = next_stock;
    }

    fprintf(stderr, "c final_stock=%.6f total_shortage=%.6f total_overflow=%.6f\n", stock, total_shortage, total_overflow);
    return EXIT_SUCCESS;
}
