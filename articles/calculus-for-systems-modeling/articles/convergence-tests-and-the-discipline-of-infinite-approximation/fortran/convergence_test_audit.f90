program convergence_test_audit
  implicit none
  real(8) :: geo, geo_ref, p125, p075
  integer :: i

  geo = 0.0d0
  do i=0,24
    geo = geo + 10.0d0 * (0.6d0 ** i)
  end do
  geo_ref = 10.0d0 / (1.0d0 - 0.6d0)

  p125 = 0.0d0
  p075 = 0.0d0
  do i=1,10000
    p125 = p125 + 1.0d0 / (real(i,8) ** 1.25d0)
    p075 = p075 + 1.0d0 / (real(i,8) ** 0.75d0)
  end do

  print '(A)', 'series_name test_used n_terms partial_sum last_term test_result estimated_error'
  print '(A,1X,A,1X,I6,1X,F12.6,1X,F12.6,1X,A,1X,F12.6)', 'geometric_r_0.6','geometric',25,geo,10.0d0*(0.6d0**24),'converges',geo_ref-geo
  print '(A,1X,A,1X,I6,1X,F12.6,1X,F12.6,1X,A)', 'p_series_1.25','p-series',10000,p125,1.0d0/(10000.0d0**1.25d0),'converges'
  print '(A,1X,A,1X,I6,1X,F12.6,1X,F12.6,1X,A)', 'p_series_0.75','p-series',10000,p075,1.0d0/(10000.0d0**0.75d0),'diverges'
end program
