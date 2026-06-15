program jacobian_audit
  implicit none
  real(8), dimension(3) :: xs, ys, dxs, dys
  real(8) :: x, y, dx, dy, j11, j12, j21, j22, detv, b1, b2, a1, a2, ac1, ac2, rc1, rc2, err
  integer :: i

  xs = (/2.0d0, 2.0d0, 0.0d0/)
  ys = (/1.0d0, 1.0d0, 0.0d0/)
  dxs = (/0.1d0, 0.5d0, 0.1d0/)
  dys = (/-0.05d0, 0.5d0, 0.1d0/)

  print '(A)', 'x y dx dy j11 j12 j21 j22 determinant approx1 approx2 actual1 actual2 error warning'

  do i=1,3
    x = xs(i); y = ys(i); dx = dxs(i); dy = dys(i)
    j11 = 2.0d0*x; j12 = 1.0d0; j21 = y; j22 = x + 3.0d0
    detv = j11*j22 - j12*j21
    b1 = x*x + y
    b2 = x*y + 3.0d0*y
    a1 = (x+dx)*(x+dx) + (y+dy)
    a2 = (x+dx)*(y+dy) + 3.0d0*(y+dy)
    ac1 = j11*dx + j12*dy
    ac2 = j21*dx + j22*dy
    rc1 = a1 - b1
    rc2 = a2 - b2
    err = sqrt((rc1-ac1)**2 + (rc2-ac2)**2)
    if (abs(detv) > 1.0d-8) then
      print '(14F12.6,1X,A)', x,y,dx,dy,j11,j12,j21,j22,detv,ac1,ac2,rc1,rc2,err,'ok'
    else
      print '(14F12.6,1X,A)', x,y,dx,dy,j11,j12,j21,j22,detv,ac1,ac2,rc1,rc2,err,'singular'
    end if
  end do
end program
