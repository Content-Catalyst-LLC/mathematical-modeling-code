program span_basis_audit
  implicit none
  real :: det
  integer :: rank_value
  logical :: spans, independent, basis
  real, dimension(3,3) :: m

  m = reshape((/ &
       1.0, 0.0, 0.0, &
       0.0, 1.0, 0.0, &
       0.5, 0.5, 1.0 /), (/3,3/))

  det = m(1,1)*(m(2,2)*m(3,3)-m(2,3)*m(3,2)) &
      - m(1,2)*(m(2,1)*m(3,3)-m(2,3)*m(3,1)) &
      + m(1,3)*(m(2,1)*m(3,2)-m(2,2)*m(3,1))

  if (abs(det) > 1.0e-10) then
     rank_value = 3
  else
     rank_value = 2
  end if

  spans = rank_value == 3
  independent = rank_value == 3
  basis = spans .and. independent

  print *, "vector_set_name ambient_dimension vector_count rank spans independent basis"
  print *, "candidate_system_basis", 3, 3, rank_value, spans, independent, basis
end program span_basis_audit
