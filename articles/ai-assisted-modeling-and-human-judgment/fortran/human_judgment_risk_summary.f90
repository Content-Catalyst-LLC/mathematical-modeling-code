program human_judgment_risk_summary
  implicit none

  integer, parameter :: n = 4
  character(len=32) :: keys(n)
  real(8) :: evidence(n), uncertainty(n), consequence(n), automation(n), accountability(n)
  real(8) :: score(n)
  integer :: i

  keys = (/ 'problem_frame                 ', 'data_fit                      ', &
            'model_use                     ', 'public_summary                ' /)

  evidence = (/ 0.72d0, 0.62d0, 0.68d0, 0.76d0 /)
  uncertainty = (/ 0.58d0, 0.66d0, 0.70d0, 0.62d0 /)
  consequence = (/ 0.80d0, 0.75d0, 0.88d0, 0.82d0 /)
  automation = (/ 0.45d0, 0.50d0, 0.72d0, 0.60d0 /)
  accountability = (/ 0.70d0, 0.65d0, 0.55d0, 0.72d0 /)

  print '(A)', 'key evidence uncertainty consequence automation_bias accountability_clarity judgment_risk_score'

  do i = 1, n
    score(i) = judgment_risk_score(evidence(i), uncertainty(i), consequence(i), automation(i), accountability(i))
    print '(A,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F8.4,1X,F10.4)', &
      trim(keys(i)), evidence(i), uncertainty(i), consequence(i), automation(i), accountability(i), score(i)
  end do

contains

  real(8) function judgment_risk_score(evidence, uncertainty, consequence, automation, accountability)
    implicit none
    real(8), intent(in) :: evidence, uncertainty, consequence, automation, accountability
    judgment_risk_score = 0.25d0 * (1.0d0 - evidence) + 0.25d0 * uncertainty + 0.25d0 * consequence + 0.15d0 * automation + 0.10d0 * (1.0d0 - accountability)
  end function judgment_risk_score

end program human_judgment_risk_summary
