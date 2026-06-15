#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double objective(double x, double y){ return x*x + 2.0*y*y; }

int main(){
  std::vector<double> targets = {12.0, 18.0, 24.0};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "x,y,objective_value,constraint_value,constraint_target,constraint_residual,lambda_value,gradient_f_x,gradient_f_y,gradient_g_x,gradient_g_y,stationarity_residual_norm,feasible,warning\n";
  for(double target : targets){
    double y = target / 3.0;
    double x = 2.0 * target / 3.0;
    double lambda = 2.0 * x;
    double gfx = 2.0*x, gfy = 4.0*y, ggx = 1.0, ggy = 1.0;
    double sx = gfx - lambda*ggx, sy = gfy - lambda*ggy;
    double norm = std::sqrt(sx*sx + sy*sy);
    double cval = x + y;
    double cres = cval - target;
    bool feasible = std::abs(cres) <= 1e-9;
    std::string warning = feasible && norm <= 1e-8 ? "Multiplier interpretation is local and unit-dependent." : "Review feasibility or stationarity.";
    std::cout << x << "," << y << "," << objective(x,y) << "," << cval << "," << target << "," << cres << "," << lambda << "," << gfx << "," << gfy << "," << ggx << "," << ggy << "," << norm << "," << feasible << "," << warning << "\n";
  }
}
