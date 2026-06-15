#include <algorithm>
#include <iomanip>
#include <iostream>
#include <utility>

std::pair<double,double> rates(double prey, double predator, double alpha, double beta, double delta, double gamma){
  return {alpha*prey - beta*prey*predator, delta*prey*predator - gamma*predator};
}

int main(){
  double prey = 40.0, predator = 9.0, alpha = 0.7, beta = 0.05, delta = 0.02, gamma = 0.5, dt = 0.01;
  int steps = 2000;
  std::cout << std::fixed << std::setprecision(6);
  std::cout << "scenario,time,prey,predator,prey_rate,predator_rate,alpha,beta,delta,gamma,method,warning\n";
  for(int n=0; n<=steps; n++){
    double t = n*dt;
    auto [prey_rate, predator_rate] = rates(prey, predator, alpha, beta, delta, gamma);
    std::cout << "predator_prey_coupled_system," << t << "," << prey << "," << predator << "," << prey_rate << "," << predator_rate << ","
              << alpha << "," << beta << "," << delta << "," << gamma << ",explicit_euler,Predator-prey terms are illustrative and assume continuous well-mixed interaction.\n";
    prey = std::max(0.0, prey + dt*prey_rate);
    predator = std::max(0.0, predator + dt*predator_rate);
  }
}
