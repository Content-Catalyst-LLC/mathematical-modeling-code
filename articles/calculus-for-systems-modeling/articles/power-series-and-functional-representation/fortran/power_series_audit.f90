program power_series_audit
  implicit none
  real(8), dimension(3) :: xs
  integer, dimension(3) :: ns
  real(8) :: x, partial, reference
  integer :: i, n, n_terms

  xs = (/0.25d0, 0.75d0, 1.25d0/)
  ns = (/5, 20, 10/)

  print '(A)', 'function_name center x_value n_terms partial_sum reference_value absolute_error convergence_status'

  do i=1,3
    x = xs(i)
    n_terms = ns(i)
    partial = 0.0d0
    do n=0,n_terms-1
      partial = partial + x**n
    end do

    if (abs(x) < 1.0d0) then
      reference = 1.0d0 / (1.0d0 - x)
      print '(A,1X,F5.1,1X,F8.4,1X,I4,1X,F14.8,1X,F14.8,1X,F14.8,1X,A)', '1/(1-x)', 0.0d0, x, n_terms, partial, reference, abs(reference-partial), 'inside_radius'
    else
      print '(A,1X,F5.1,1X,F8.4,1X,I4,1X,F14.8,1X,A)', '1/(1-x)', 0.0d0, x, n_terms, partial, 'outside_radius'
    end if
  end do
end program
