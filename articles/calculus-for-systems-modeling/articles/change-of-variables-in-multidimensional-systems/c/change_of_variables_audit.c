#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define PI 3.14159265358979323846

double exposure_cartesian(double x, double y){
  double r = sqrt(x*x + y*y);
  return 20.0 * exp(-0.4 * r);
}

double exposure_polar(double r, double theta){
  (void)theta;
  return 20.0 * exp(-0.4 * r);
}

double polar_total(double radius, double dr, double dtheta){
  double total = 0.0;
  for(double r = dr / 2.0; r < radius; r += dr){
    for(double theta = dtheta / 2.0; theta < 2.0 * PI; theta += dtheta){
      total += exposure_polar(r, theta) * r * dr * dtheta;
    }
  }
  return total;
}

double cartesian_grid_total(double radius, double step){
  double total = 0.0;
  int n = (int)((2.0 * radius) / step);
  for(int i=0; i<=n; i++){
    double x = -radius + i * step;
    for(int j=0; j<=n; j++){
      double y = -radius + j * step;
      if(x*x + y*y <= radius*radius){
        total += exposure_cartesian(x,y) * step * step;
      }
    }
  }
  return total;
}

void audit(double radius, double dr, double dtheta, const char* scenario){
  double p = polar_total(radius, dr, dtheta);
  double c = cartesian_grid_total(radius, dr);
  double diff = fabs(p - c);
  double rel = diff / fmax(fabs(p), 1e-12);
  const char* warning = dr > 0.5 ? "Resolution is coarse; transformed and Cartesian approximations may differ." : "Polar Jacobian factor r included; compare domain and resolution assumptions.";
  printf("%s,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%s,%s\n", scenario, radius, dr, dtheta, p, c, diff, rel, "dA = r dr dtheta", warning);
}

int main(void){
  printf("scenario,radius,radial_step,angular_step,polar_total,cartesian_grid_total,absolute_difference,relative_difference,jacobian_rule,warning\n");
  audit(3.0, 0.5, PI / 24.0, "medium_polar_grid");
  audit(3.0, 0.25, PI / 48.0, "fine_polar_grid");
  audit(3.0, 0.125, PI / 96.0, "very_fine_polar_grid");
  return EXIT_SUCCESS;
}
