#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

std::string classify(double d){
  if(d < -1e-8) return "locally_stable";
  if(d > 1e-8) return "locally_unstable";
  return "inconclusive_at_critical_value";
}

int main(){
  std::cout << std::fixed << std::setprecision(6);
  std::cout << "model,parameter_mu,equilibrium,derivative_value,stability,branch_status,warning\n";
  for(int step=-20; step<=40; step++){
    double mu = step / 10.0;
    if(mu < 0.0){
      std::cout << "saddle_node_normal_form," << mu << ",,,no_real_equilibrium,equilibrium_absent,For mu below zero the saddle-node normal form has no real equilibrium.\n";
    } else if(std::abs(mu) < 1e-12){
      double eq = 0.0;
      double d = -2.0 * eq;
      std::cout << "saddle_node_normal_form," << mu << "," << eq << "," << d << "," << classify(d) << ",critical_branch,Bifurcation interpretation depends on model form parameter meaning and domain validity.\n";
    } else {
      double root = std::sqrt(mu);
      for(double eq : std::vector<double>{-root, root}){
        double d = -2.0 * eq;
        std::cout << "saddle_node_normal_form," << mu << "," << eq << "," << d << "," << classify(d) << ",equilibrium_present,Bifurcation interpretation depends on model form parameter meaning and domain validity.\n";
      }
    }
  }
}
