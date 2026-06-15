program sequence_series_convergence_audit
  implicit none
  real(8) :: geo, geo_ref, harm
  integer :: i

  geo = 0.0d0
  do i=0,24
    geo = geo + 10.0d0 * (0.6d0 ** i)
  end do
  geo_ref = 10.0d0 / (1.0d0 - 0.6d0)

  harm = 0.0d0
  do i=1,10000
    harm = harm + 1.0d0 / real(i,8)
  end do

  print '(A)', 'series_name n_terms last_term partial_sum reference_value estimated_error classification'
  print '(A,1X,I6,1X,F12.6,1X,F12.6,1X,F12.6,1X,F12.6,1X,A)', 'geometric_r_0.6',25,10.0d0*(0.6d0**24),geo,geo_ref,geo_ref-geo,'convergent'
  print '(A,1X,I6,1X,F12.6,1X,F12.6,1X,A)', 'harmonic',10000,1.0d0/10000.0d0,harm,'divergent'
end program
