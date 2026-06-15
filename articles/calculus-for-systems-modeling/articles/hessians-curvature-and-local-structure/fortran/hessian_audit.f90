program hessian_audit
  implicit none
  real(8), dimension(3) :: xs, ys, dxs, dys
  real(8) :: x, y, dx, dy, gx, gy, h11, h12, h21, h22, detv, first, second, actual, quad
  integer :: i
  character(len=40) :: classv
  character(len=80) :: warning

  xs = (/2.0d0, 2.0d0, -5.0d0/)
  ys = (/1.0d0, 1.0d0, 0.0d0/)
  dxs = (/0.1d0, 0.5d0, 0.2d0/)
  dys = (/-0.05d0, 0.5d0, 0.1d0/)

  print '(A)', 'x y dx dy gx gy h11 h12 h21 h22 determinant trace classification first second actual error1 error2 warning'

  do i=1,3
    x = xs(i); y = ys(i); dx = dxs(i); dy = dys(i)
    gx = 2.0d0*x + y + 0.4d0*x*y
    gy = x + 6.0d0*y + 0.2d0*x*x
    h11 = 2.0d0 + 0.4d0*y
    h12 = 1.0d0 + 0.4d0*x
    h21 = h12
    h22 = 6.0d0
    detv = h11*h22 - h12*h21
    if (detv > 0.0d0 .and. h11 > 0.0d0) then
      classv = 'positive_definite'
    else if (detv > 0.0d0 .and. h11 < 0.0d0) then
      classv = 'negative_definite'
    else if (detv < 0.0d0) then
      classv = 'indefinite'
    else
      classv = 'inconclusive'
    end if
    first = gx*dx + gy*dy
    quad = 0.5d0*(h11*dx*dx + 2.0d0*h12*dx*dy + h22*dy*dy)
    second = first + quad
    actual = f_model(x+dx,y+dy) - f_model(x,y)
    if (detv < 0.0d0) then
      warning = 'saddle_like'
    else if (abs(detv) < 1.0d-8) then
      warning = 'singular'
    else
      warning = 'ok'
    end if
    print '(12F12.6,1X,A,5F12.6,1X,A)', x,y,dx,dy,gx,gy,h11,h12,h21,h22,detv,h11+h22,trim(classv),first,second,actual,abs(actual-first),abs(actual-second),trim(warning)
  end do

contains
  function f_model(x,y) result(value)
    real(8), intent(in) :: x, y
    real(8) :: value
    value = x*x + x*y + 3.0d0*y*y + 0.2d0*x*x*y
  end function f_model
end program
