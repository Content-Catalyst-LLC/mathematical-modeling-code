#include <cmath>
#include <iomanip>
#include <iostream>

double restoring_rate(double x, double equilibrium, double recovery_rate){ return -recovery_rate * (x - equilibrium); }
double impulse_shock(double time, double shock_time, double shock_magnitude){ return std::abs(time - shock_time) < 1e-12 ? shock_magnitude : 0.0; }

int main(){
  double baseline = 100.0, forced = 100.0;
  double equilibrium = 100.0, recovery_rate = 0.15, shock_time = 10.0, shock_magnitude = -30.0, dt = 0.1;
  std::cout << std::fixed << std::setprecision(6);
  std::cout << "step,time,baseline_state,forced_state,shock_value,absolute_deviation,warning\n";
  for(int step=0; step<=300; step++){
    double time = step * dt;
    double shock = impulse_shock(time, shock_time, shock_magnitude);
    std::cout << step << "," << time << "," << baseline << "," << forced << "," << shock << "," << std::abs(forced-baseline) << ",Shock response depends on forcing form timing magnitude recovery rate and numerical step size.\n";
    baseline = baseline + dt * restoring_rate(baseline, equilibrium, recovery_rate);
    if(shock != 0.0){ forced = forced + shock; }
    forced = forced + dt * restoring_rate(forced, equilibrium, recovery_rate);
  }
}
