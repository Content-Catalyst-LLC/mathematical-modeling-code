program network_graph_diagnostics
  implicit none

  integer, parameter :: n = 7, m = 10
  integer :: source(m), target(m)
  real(8) :: weight(m)
  integer :: in_degree(n), out_degree(n)
  real(8) :: weighted_out(n)
  integer :: i

  source = (/1, 1, 2, 3, 4, 4, 5, 6, 2, 1/)
  target = (/7, 5, 7, 1, 7, 3, 7, 7, 6, 2/)
  weight = (/0.95d0, 0.90d0, 0.70d0, 0.60d0, 0.50d0, 0.65d0, 0.80d0, 0.75d0, 0.55d0, 0.85d0/)

  in_degree = 0
  out_degree = 0
  weighted_out = 0.0d0

  do i = 1, m
    out_degree(source(i)) = out_degree(source(i)) + 1
    in_degree(target(i)) = in_degree(target(i)) + 1
    weighted_out(source(i)) = weighted_out(source(i)) + weight(i)
  end do

  print '(A,I0,A,I0)', 'fortran node_count=', n, ' edge_count=', m

  do i = 1, n
    print '(A,I0,A,I0,A,I0,A,F6.2)', 'node=', i, ' in_degree=', in_degree(i), ' out_degree=', out_degree(i), ' weighted_out=', weighted_out(i)
  end do
end program network_graph_diagnostics
