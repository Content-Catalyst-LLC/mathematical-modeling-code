program domain_range_validation
  implicit none
  print '(A)', 'scenario status value_or_issue'
  call report('baseline', 10.0d0, 0.20d0, 100.0d0, 20.0d0)
  call report('near_capacity', 95.0d0, 0.20d0, 100.0d0, 20.0d0)
  call report('invalid_negative_state', -5.0d0, 0.20d0, 100.0d0, 20.0d0)
  call report('outside_capacity', 120.0d0, 0.20d0, 100.0d0, 20.0d0)
contains
  subroutine report(name, initial_state, rate, capacity, time_horizon)
    character(len=*), intent(in) :: name
    real(8), intent(in) :: initial_state, rate, capacity, time_horizon
    real(8) :: value
    if (initial_state < 0.0d0) then
      print '(A,1X,A,1X,A)', trim(name), 'domain_review', 'initial_state_must_be_nonnegative'
    else if (rate < 0.0d0) then
      print '(A,1X,A,1X,A)', trim(name), 'domain_review', 'rate_must_be_nonnegative'
    else if (capacity <= 0.0d0) then
      print '(A,1X,A,1X,A)', trim(name), 'domain_review', 'capacity_must_be_positive'
    else if (time_horizon < 0.0d0) then
      print '(A,1X,A,1X,A)', trim(name), 'domain_review', 'time_horizon_must_be_nonnegative'
    else if (initial_state > capacity) then
      print '(A,1X,A,1X,A)', trim(name), 'domain_review', 'initial_state_exceeds_capacity'
    else
      value = capacity / (1.0d0 + ((capacity - initial_state) / initial_state) * exp(-rate * time_horizon))
      print '(A,1X,A,1X,F10.6)', trim(name), 'ok', value
    end if
  end subroutine report
end program domain_range_validation
