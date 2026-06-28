program solution_space_audit
  implicit none
  integer :: variable_count
  integer :: equation_count
  integer :: rank_value
  integer :: nullity_value

  variable_count = 4
  equation_count = 3
  rank_value = 3
  nullity_value = variable_count - rank_value

  print *, "system_name variable_count equation_count rank nullity"
  print *, "four_variable_three_constraint_system", variable_count, equation_count, rank_value, nullity_value
end program solution_space_audit
