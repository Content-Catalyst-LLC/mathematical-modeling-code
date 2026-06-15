program flux_circulation_audit
  implicit none
  print '(A)', 'scenario segment_count approximate_flux approximate_circulation mean_tangential_alignment mean_normal_alignment field_description geometry_description warning'
  call audit(1.0d0, 16, 'coarse_circle')
  call audit(1.0d0, 64, 'medium_circle')
  call audit(1.0d0, 256, 'fine_circle')
contains
  subroutine audit(radius, segments, scenario)
    real(8), intent(in) :: radius
    integer, intent(in) :: segments
    character(len=*), intent(in) :: scenario
    integer :: i
    real(8) :: theta0,theta1,x0,y0,x1,y1,xm,ym,dx,dy,seglen,tx,ty,nx,ny,fx,fy
    real(8) :: flux_total,circulation_total,tangent_sum,normal_sum,pi
    character(len=32) :: warning
    pi = 4.0d0*atan(1.0d0)
    flux_total=0.0d0; circulation_total=0.0d0; tangent_sum=0.0d0; normal_sum=0.0d0
    do i=0,segments-1
      theta0 = 2.0d0*pi*i/segments
      theta1 = 2.0d0*pi*(i+1)/segments
      x0 = radius*cos(theta0); y0 = radius*sin(theta0)
      x1 = radius*cos(theta1); y1 = radius*sin(theta1)
      xm = 0.5d0*(x0+x1); ym = 0.5d0*(y0+y1)
      dx = x1-x0; dy = y1-y0
      seglen = sqrt(dx*dx+dy*dy)
      tx = dx/seglen; ty = dy/seglen
      nx = xm/radius; ny = ym/radius
      fx = -ym; fy = xm
      circulation_total = circulation_total + fx*dx + fy*dy
      flux_total = flux_total + (fx*nx + fy*ny)*seglen
      tangent_sum = tangent_sum + fx*tx + fy*ty
      normal_sum = normal_sum + fx*nx + fy*ny
    end do
    if (segments < 32) then
      warning = 'coarse_path'
    else
      warning = 'synthetic_flow'
    end if
    print '(A,1X,I8,4F14.6,1X,A,1X,A,1X,A)', trim(scenario), segments, flux_total, circulation_total, tangent_sum/segments, normal_sum/segments, 'field', 'circle', trim(warning)
  end subroutine
end program
