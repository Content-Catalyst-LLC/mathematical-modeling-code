#include <math.h>
#include <stdio.h>
#include <stdlib.h>

void vector_field(double x, double y, double* fx, double* fy){ *fx = -y; *fy = x; }
double dot2(double ax,double ay,double bx,double by){ return ax*bx + ay*by; }

void audit(double radius, int segments, const char* scenario){
  double flux_total = 0.0, circulation_total = 0.0, tangent_sum = 0.0, normal_sum = 0.0;
  for(int i=0; i<segments; i++){
    double theta0 = 2.0*M_PI*i/segments;
    double theta1 = 2.0*M_PI*(i+1)/segments;
    double x0 = radius*cos(theta0), y0 = radius*sin(theta0);
    double x1 = radius*cos(theta1), y1 = radius*sin(theta1);
    double xm = 0.5*(x0+x1), ym = 0.5*(y0+y1);
    double dx = x1-x0, dy = y1-y0;
    double segment_length = sqrt(dx*dx + dy*dy);
    double tx = dx/segment_length, ty = dy/segment_length;
    double nx = xm/radius, ny = ym/radius;
    double fx, fy;
    vector_field(xm, ym, &fx, &fy);
    circulation_total += dot2(fx, fy, dx, dy);
    flux_total += dot2(fx, fy, nx, ny) * segment_length;
    tangent_sum += dot2(fx, fy, tx, ty);
    normal_sum += dot2(fx, fy, nx, ny);
  }
  const char* warning = segments < 32 ? "Coarse path sampling; circulation and flux should be checked with more segments." : "Synthetic flow audit; document field meaning orientation units and boundary choice.";
  printf("%s,%d,%.12f,%.12f,%.12f,%.12f,%s,%s,%s\n", scenario, segments, flux_total, circulation_total, tangent_sum/segments, normal_sum/segments, "rotating field F=<-y,x>", "counterclockwise circle with radius 1", warning);
}

int main(void){
  printf("scenario,segment_count,approximate_flux,approximate_circulation,mean_tangential_alignment,mean_normal_alignment,field_description,geometry_description,warning\n");
  audit(1.0, 16, "coarse_circle");
  audit(1.0, 64, "medium_circle");
  audit(1.0, 256, "fine_circle");
  return EXIT_SUCCESS;
}
