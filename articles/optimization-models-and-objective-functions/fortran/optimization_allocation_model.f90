program optimization_allocation_model
  implicit none

  integer :: a, b, c, d, feasible_count, candidate_count
  integer :: best_a, best_b, best_c, best_d
  real(8) :: budget, total_cost, total_benefit, best_benefit
  integer :: equity_floor

  budget = 75.0d0
  equity_floor = 1
  feasible_count = 0
  candidate_count = 0
  best_benefit = -1.0d0
  best_a = 0
  best_b = 0
  best_c = 0
  best_d = 0

  do a = 0, 8
    do b = 0, 8
      do c = 0, 8
        do d = 0, 8
          candidate_count = candidate_count + 1
          total_cost = 7.0d0*a + 8.0d0*b + 5.0d0*c + 6.0d0*d
          total_benefit = 11.0d0*a + 13.0d0*b + 8.0d0*c + 10.0d0*d

          if (total_cost <= budget .and. a >= equity_floor .and. b >= equity_floor .and. c >= equity_floor .and. d >= equity_floor) then
            feasible_count = feasible_count + 1
            if (total_benefit > best_benefit) then
              best_benefit = total_benefit
              best_a = a
              best_b = b
              best_c = c
              best_d = d
            end if
          end if

        end do
      end do
    end do
  end do

  print '(A,I0,A,I0,A,F10.2,A,4(I0,1X))', 'fortran candidates=', candidate_count, ' feasible=', feasible_count, ' best_benefit=', best_benefit, ' best_allocation=', best_a, best_b, best_c, best_d
end program optimization_allocation_model
