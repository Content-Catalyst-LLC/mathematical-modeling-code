#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double f(double x, double y){ return 3.0*x + 2.0*y + 0.5*x*y; }
double fx(double, double y){ return 3.0 + 0.5*y; }
double fy(double x, double){ return 2.0 + 0.5*x; }
double total_differential(double x, double y, double dx, double dy){ return fx(x,y)*dx + fy(x,y)*dy; }
bool feasible_displacement(double x, double y, double dx, double dy){ return x >= 0.0 && y >= 0.0 && x + y <= 10.0 && x + dx >= 0.0 && y + dy >= 0.0 && x + dx + y + dy <= 10.0; }

int main(){
  std::vector<std::vector<double>> cases = {{4.0,3.0,0.2,-0.1},{4.0,3.0,1.0,1.0},{8.0,1.0,1.0,1.0}};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "x,y,dx,dy,baseline_output,actual_output,actual_change,differential_estimate,absolute_error,feasible_displacement,warning\n";
  for(auto row : cases){
    double x=row[0], y=row[1], dx=row[2], dy=row[3];
    double baseline=f(x,y), actual=f(x+dx,y+dy), change=actual-baseline, estimate=total_differential(x,y,dx,dy);
    bool feasible=feasible_displacement(x,y,dx,dy);
    std::cout << x << "," << y << "," << dx << "," << dy << "," << baseline << "," << actual << "," << change << "," << estimate << "," << std::abs(change-estimate) << "," << feasible << "," << (feasible ? "" : "Displacement is outside the feasible region.") << "\n";
  }
}
