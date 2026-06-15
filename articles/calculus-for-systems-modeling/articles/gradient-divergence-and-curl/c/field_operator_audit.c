#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double scalar_field(double x, double y){ return x*x + y*y; }
void vector_field(double x, double y, double* p, double* q){ *p = -y; *q = x; }
void gradient(double x, double y, double* gx, double* gy){ *gx = 2.0*x; *gy = 2.0*y; }
double divergence(double x, double y){ (void)x; (void)y; return 0.0; }
double curl_2d(double x, double y){ (void)x; (void)y; return 2.0; }

void audit(double step, const char* scenario){
  int n = (int)(2.0 / step) + 1;
  int count = 0;
  double grad_sum = 0.0, max_grad = 0.0, div_sum = 0.0, curl_sum = 0.0, max_abs_curl = 0.0;
  for(int i=0; i<n; i++){
    double x = -1.0 + i*step;
    for(int j=0; j<n; j++){
      double y = -1.0 + j*step;
      double gx, gy;
      gradient(x,y,&gx,&gy);
      double gmag = sqrt(gx*gx + gy*gy);
      double div = divergence(x,y);
      double curl = curl_2d(x,y);
      count++;
      grad_sum += gmag;
      if(gmag > max_grad) max_grad = gmag;
      div_sum += div;
      curl_sum += curl;
      if(fabs(curl) > max_abs_curl) max_abs_curl = fabs(curl);
    }
  }
  const char* warning = step > 0.5 ? "Grid step is coarse; local derivative structure may be undersampled." : "Synthetic field-operator audit; document field definitions units grid and boundary rules.";
  printf("%s,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%s,%s\n", scenario, step, count, grad_sum/count, max_grad, div_sum/count, curl_sum/count, max_abs_curl, "scalar f=x^2+y^2; vector F=<-y,x>", warning);
}

int main(void){
  printf("scenario,grid_step,point_count,mean_gradient_magnitude,maximum_gradient_magnitude,mean_divergence,mean_curl,maximum_abs_curl,field_description,warning\n");
  audit(1.0, "coarse_grid");
  audit(0.5, "medium_grid");
  audit(0.25, "fine_grid");
  return EXIT_SUCCESS;
}
