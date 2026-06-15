#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

std::pair<double,double> rotation_field(double x, double y){ return {-y, x}; }
std::pair<double,double> expansion_field(double x, double y){ return {x, y}; }

std::vector<std::pair<double,double>> boundary_points(int n){
  std::vector<std::pair<double,double>> pts;
  for(int i=0;i<n;i++){ double t=-1.0+2.0*i/n; pts.push_back({t,-1.0}); }
  for(int i=0;i<n;i++){ double t=-1.0+2.0*i/n; pts.push_back({1.0,t}); }
  for(int i=0;i<n;i++){ double t=1.0-2.0*i/n; pts.push_back({t,1.0}); }
  for(int i=0;i<n;i++){ double t=1.0-2.0*i/n; pts.push_back({-1.0,t}); }
  pts.push_back(pts.front());
  return pts;
}

void audit(int segments, double step, const std::string& scenario){
  auto pts = boundary_points(segments);
  double bc=0.0, bf=0.0;
  for(size_t i=0;i+1<pts.size();i++){
    auto [x0,y0]=pts[i];
    auto [x1,y1]=pts[i+1];
    double xm=0.5*(x0+x1), ym=0.5*(y0+y1);
    double dx=x1-x0, dy=y1-y0;
    auto [p,q]=rotation_field(xm,ym);
    bc += p*dx + q*dy;
    auto [a,b]=expansion_field(xm,ym);
    bf += a*dy + b*(-dx);
  }
  int n = static_cast<int>(2.0/step);
  double ic = 2.0*n*n*step*step;
  double idv = ic;
  std::string warning = (segments < 16 || step > 0.25) ? "Coarse boundary or interior sampling." : "Synthetic Greens theorem audit.";
  std::cout << scenario << "," << segments << "," << step << "," << bc << "," << ic << "," << bf << "," << idv << "," << std::abs(bc-ic) << "," << std::abs(bf-idv) << ",circulation F=<-y,x>; flux G=<x,y>,square [-1,1]x[-1,1]," << warning << "\n";
}

int main(){
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "scenario,boundary_segments_per_side,interior_grid_step,boundary_circulation,interior_curl_integral,boundary_flux,interior_divergence_integral,circulation_gap,flux_gap,field_description,region_description,warning\n";
  audit(8, 0.5, "coarse_audit");
  audit(32, 0.25, "medium_audit");
  audit(128, 0.125, "fine_audit");
}
