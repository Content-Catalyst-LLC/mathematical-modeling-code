program communication_summary
  implicit none

  integer, parameter :: n = 5
  character(len=32) :: keys(n), layers(n), audiences(n), statuses(n)
  real(8) :: scores(n)
  integer :: i

  keys = (/ 'central_result                 ', 'uncertainty_range              ', 'threshold_risk                 ', 'structural_limit               ', 'use_limit                      ' /)
  layers = (/ 'result                         ', 'uncertainty                    ', 'decision_threshold             ', 'model_limit                    ', 'governance                     ' /)
  audiences = (/ 'decision_maker                ', 'public                        ', 'decision_maker                ', 'technical_reviewer            ', 'future_user                   ' /)
  statuses = (/ 'active                        ', 'review                        ', 'review                        ', 'review                        ', 'review                        ' /)

  print '(A)', 'key layer audience status priority'

  do i = 1, n
    scores(i) = priority(trim(layers(i)), trim(audiences(i)), trim(statuses(i)))
    print '(A,1X,A,1X,A,1X,A,1X,F6.2)', trim(keys(i)), trim(layers(i)), trim(audiences(i)), trim(statuses(i)), scores(i)
  end do

contains

  real(8) function priority(layer, audience, status)
    implicit none
    character(len=*), intent(in) :: layer, audience, status

    if (status == 'active') then
      priority = 1.0d0
    else
      priority = 5.0d0
    end if

    if (layer == 'decision_threshold' .or. layer == 'governance' .or. layer == 'model_limit') then
      priority = priority + 2.0d0
    end if

    if (audience == 'public' .or. audience == 'decision_maker') then
      priority = priority + 1.0d0
    end if
  end function priority

end program communication_summary
