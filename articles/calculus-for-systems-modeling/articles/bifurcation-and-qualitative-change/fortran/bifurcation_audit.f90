program bifurcation_audit
  implicit none
  integer :: step, i
  real(8) :: mu, root, eq, d
  real(8), dimension(2) :: eqs
  print '(A)', 'model parameter_mu equilibrium derivative_value stability branch_status'
  do step = -20, 40
    mu = dble(step) / 10.0d0
    if (mu < 0.0d0) then
      print '(A,F12.6,1X,A)', 'saddle_node_normal_form', mu, 'no_real_equilibrium equilibrium_absent'
    else if (abs(mu) < 1.0d-12) then
      eq = 0.0d0
      d = -2.0d0 * eq
      print '(A,F12.6,2F12.6,1X,A,1X,A)', 'saddle_node_normal_form', mu, eq, d, trim(classify(d)), 'critical_branch'
    else
      root = sqrt(mu)
      eqs = (/ -root, root /)
      do i = 1, 2
        eq = eqs(i)
        d = -2.0d0 * eq
        print '(A,F12.6,2F12.6,1X,A,1X,A)', 'saddle_node_normal_form', mu, eq, d, trim(classify(d)), 'equilibrium_present'
      end do
    end if
  end do
contains
  character(len=32) function classify(d)
    real(8), intent(in) :: d
    if (d < -1.0d-8) then
      classify = 'locally_stable'
    else if (d > 1.0d-8) then
      classify = 'locally_unstable'
    else
      classify = 'inconclusive_at_critical_value'
    end if
  end function
end program
