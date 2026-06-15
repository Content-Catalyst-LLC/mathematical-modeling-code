#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <utility>

double scalar_field(double x, double y){ return x*x + y*y; }
std::pair<double,double> vector_field(double x, double y){ return {-y, x}; }
std::pair<double,double> gradient(double x, double y){ return {2.0*x, 2.0*y}; }
double divergence(double x, double y){ (void)x; (void)y; return 0.0; }
double curl_2d(double x, double y){ (void)x; (void)y; return 2.0; }

void audit(double step, const std::string& scenario){
  int n = static_cast<int>(2.0 / step) + 1;
  int count = 0;
  double grad_sum = 0.0, max_grad = 0.0, div_sum = 0.0, curl_sum = 0.0, max_abs_curl = 0.0;
  for(int i=0; i<n; i++){
    double x = -1.0 + i*step;
    for(int j=0; j<n; j++){
      double y = -1.0 + j*step;
      auto [gx, gy] = gradient(x,y);
      double gmag = std::sqrt(gx*gx + gy*gy);
      double div = divergence(x,y);
      double curl = curl_2d(x,y);
      count++;
      grad_sum += gmag;
      max_grad = std::max(max_grad, gmag);
      div_sum += div;
      curl_sum += curl;
      max_abs_curl = std::max(max_abs_curl, std::abs(curl));
    }
  }
  std::string warning = step > 0.5 ? "Grid step is coarse; local derivative structure may be undersampled." : "Synthetic field-operator audit; document field definitions units grid and boundary rules.";
  std::cout << scenario << "," << step << "," << count << "," << grad_sum/count << "," << max_grad << "," << div_sum/count << "," << curl_sum/count << "," << max_abs_curl << ",scalar f=x^2+y^2; vector F=<-y,x>," << warning << "\n";
}

int main(){
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "scenario,grid_step,point_count,mean_gradient_magnitude,maximum_gradient_magnitude,mean_divergence,mean_curl,maximum_abs_curl,field_description,warning\n";
  audit(1.0, "coarse_grid");
  audit(0.5, "medium_grid");
  audit(0.25, "fine_grid");
}
