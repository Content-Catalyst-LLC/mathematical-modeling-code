#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define PI 3.14159265358979323846

void audit(double radius, int segments, int radial_steps, const char* scenario){
  double circulation = 0.0;
  for(int i=0; i<segments; i++){
    double theta0 = 2.0*PI*i/segments;
    double theta1 = 2.0*PI*(i+1)/segments;
    double x0 = radius*cos(theta0), y0 = radius*sin(theta0);
    double x1 = radius*cos(theta1), y1 = radius*sin(theta1);
    double xm = 0.5*(x0+x1), ym = 0.5*(y0+y1);
    double dx = x1-x0, dy = y1-y0;
    double fx = -ym, fy = xm;
    circulation += fx*dx + fy*dy;
  }

  double curl_flux = 0.0;
  for(int i=0; i<radial_steps; i++){
    double r0 = radius*i/radial_steps;
    double r1 = radius*(i+1)/radial_steps;
    double ring_area = PI*(r1*r1 - r0*r0);
    curl_flux += 2.0*ring_area;
  }

  const char* warning = (segments < 64 || radial_steps < 16) ? "Coarse boundary or surface sampling." : "Synthetic Stokes theorem audit.";
  printf("%s,%.12f,%d,%d,%.12f,%.12f,%.12f,%s,%s,%s,%s\n", scenario, radius, segments, radial_steps, circulation, curl_flux, fabs(circulation-curl_flux), "F=<-y,x,0>; curl F=<0,0,2>", "horizontal disk with upward normal", "counterclockwise boundary orientation viewed from positive z", warning);
}

int main(void){
  printf("scenario,radius,boundary_segments,radial_steps,boundary_circulation,surface_curl_flux,absolute_gap,field_description,surface_description,orientation_note,warning\n");
  audit(1.0, 32, 8, "coarse_audit");
  audit(1.0, 128, 32, "medium_audit");
  audit(1.0, 512, 128, "fine_audit");
  return EXIT_SUCCESS;
}
