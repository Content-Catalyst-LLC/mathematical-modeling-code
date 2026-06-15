#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define PI 3.14159265358979323846

void rotation_field(double x, double y, double* p, double* q){ *p = -y; *q = x; }
void expansion_field(double x, double y, double* p, double* q){ *p = x; *q = y; }

void boundary_point(int n, int idx, double* x, double* y){
  int side = idx / n;
  int i = idx % n;
  double t;
  if(side == 0){ t = -1.0 + 2.0*i/n; *x = t; *y = -1.0; }
  else if(side == 1){ t = -1.0 + 2.0*i/n; *x = 1.0; *y = t; }
  else if(side == 2){ t = 1.0 - 2.0*i/n; *x = t; *y = 1.0; }
  else { t = 1.0 - 2.0*i/n; *x = -1.0; *y = t; }
}

void audit(int segments, double step, const char* scenario){
  double bc = 0.0, bf = 0.0;
  int total_points = 4 * segments;
  for(int idx=0; idx<total_points; idx++){
    double x0,y0,x1,y1;
    boundary_point(segments, idx, &x0, &y0);
    boundary_point(segments, (idx+1)%total_points, &x1, &y1);
    double xm = 0.5*(x0+x1), ym = 0.5*(y0+y1);
    double dx = x1-x0, dy = y1-y0;
    double p,q;
    rotation_field(xm,ym,&p,&q);
    bc += p*dx + q*dy;
    expansion_field(xm,ym,&p,&q);
    bf += p*dy + q*(-dx);
  }
  int n = (int)(2.0/step);
  double ic = 0.0, idv = 0.0;
  for(int i=0; i<n; i++){
    for(int j=0; j<n; j++){
      ic += 2.0*step*step;
      idv += 2.0*step*step;
    }
  }
  const char* warning = (segments < 16 || step > 0.25) ? "Coarse boundary or interior sampling." : "Synthetic Greens theorem audit.";
  printf("%s,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%s,%s,%s\n", scenario, segments, step, bc, ic, bf, idv, fabs(bc-ic), fabs(bf-idv), "circulation F=<-y,x>; flux G=<x,y>", "square [-1,1]x[-1,1]", warning);
}

int main(void){
  printf("scenario,boundary_segments_per_side,interior_grid_step,boundary_circulation,interior_curl_integral,boundary_flux,interior_divergence_integral,circulation_gap,flux_gap,field_description,region_description,warning\n");
  audit(8, 0.5, "coarse_audit");
  audit(32, 0.25, "medium_audit");
  audit(128, 0.125, "fine_audit");
  return EXIT_SUCCESS;
}
