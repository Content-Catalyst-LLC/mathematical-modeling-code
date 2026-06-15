#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

int main(){
  const double initial_state = 80.0, target = 100.0, adjustment_rate = 0.2, delay = 5.0, dt = 0.1;
  const int steps = 300;
  const int delay_steps = static_cast<int>(std::round(delay / dt));
  std::vector<double> states;
  states.push_back(initial_state);

  std::cout << std::fixed << std::setprecision(6);
  std::cout << "step,time,current_state,delayed_state,derivative_value,target,absolute_gap,warning\n";
  for(int step=0; step<=steps; step++){
    double time = step * dt;
    double current = states.back();
    int delayed_index = step - delay_steps;
    double delayed = delayed_index < 0 ? initial_state : states.at(static_cast<size_t>(delayed_index));
    double derivative = adjustment_rate * (target - delayed);
    std::cout << step << "," << time << "," << current << "," << delayed << "," << derivative << "," << target << "," << std::abs(current-target) << ",Delayed adjustment depends on delay length history function time step and feedback strength.\n";
    states.push_back(current + dt * derivative);
  }
}
