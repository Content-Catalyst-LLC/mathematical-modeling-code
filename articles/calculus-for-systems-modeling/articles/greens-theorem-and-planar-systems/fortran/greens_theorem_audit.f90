program greens_theorem_audit
  implicit none
  print '(A)', 'scenario boundary_segments_per_side interior_grid_step boundary_circulation interior_curl_integral boundary_flux interior_divergence_integral circulation_gap flux_gap field_description region_description warning'
  call audit(8, 0.5d0, 'coarse_audit')
  call audit(32, 0.25d0, 'medium_audit')
  call audit(128, 0.125d0, 'fine_audit')
contains
  subroutine boundary_point(n, idx, x, y)
    integer, intent(in) :: n, idx
    real(8), intent(out) :: x, y
    integer :: side, i
    real(8) :: t
    side = idx / n
    i = mod(idx, n)
    if (side == 0) then
      t = -1.0d0 + 2.0d0*i/n; x = t; y = -1.0d0
    else if (side == 1) then
      t = -1.0d0 + 2.0d0*i/n; x = 1.0d0; y = t
    else if (side == 2) then
      t = 1.0d0 - 2.0d0*i/n; x = t; y = 1.0d0
    else
      t = 1.0d0 - 2.0d0*i/n; x = -1.0d0; y = t
    end if
  end subroutine

  subroutine audit(segments, step, scenario)
    integer, intent(in) :: segments
    real(8), intent(in) :: step
    character(len=*), intent(in) :: scenario
    integer :: idx, total_points, n
    real(8) :: x0,y0,x1,y1,xm,ym,dx,dy,bc,bf,ic,idv,p,q
    character(len=32) :: warning
    bc = 0.0d0; bf = 0.0d0
    total_points = 4*segments
    do idx = 0, total_points-1
      call boundary_point(segments, idx, x0, y0)
      call boundary_point(segments, mod(idx+1,total_points), x1, y1)
      xm = 0.5d0*(x0+x1); ym = 0.5d0*(y0+y1)
      dx = x1-x0; dy = y1-y0
      p = -ym; q = xm
      bc = bc + p*dx + q*dy
      p = xm; q = ym
      bf = bf + p*dy + q*(-dx)
    end do
    n = int(2.0d0/step)
    ic = 2.0d0*n*n*step*step
    idv = ic
    if (segments < 16 .or. step > 0.25d0) then
      warning = 'coarse_audit'
    else
      warning = 'synthetic_audit'
    end if
    print '(A,1X,I8,7F14.6,1X,A,1X,A,1X,A)', trim(scenario), segments, step, bc, ic, bf, idv, abs(bc-ic), abs(bf-idv), 'field', 'square', trim(warning)
  end subroutine
end program
