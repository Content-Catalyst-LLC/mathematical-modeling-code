#include <algorithm>
#include <iostream>

int main(){
  double alpha=0.6, beta=0.02, gamma=0.5, delta=0.01;
  double x=40.0, y=9.0, dt=0.02;
  int steps=4000;
  for(int i=0;i<steps;i++){
    double dx = alpha*x - beta*x*y;
    double dy = delta*x*y - gamma*y;
    x = std::max(0.0, x + dt*dx);
    y = std::max(0.0, y + dt*dy);
  }
  std::cout << "scenario_name,model_type,final_prey,final_predator,warning\n";
  std::cout << "classic_lotka_volterra,lotka_volterra," << x << "," << y << ",mass_action_baseline\n";
}
