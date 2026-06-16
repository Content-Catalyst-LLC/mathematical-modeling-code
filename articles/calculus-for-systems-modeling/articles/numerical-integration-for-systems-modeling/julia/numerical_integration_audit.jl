rate(t)=2.0+sin(t)+0.1*t
trueint(t)=2.0*t-cos(t)+1.0+0.05*t^2
h=0.1; left=0.0; trap=0.0
println("index,time,rate,left_cumulative,trapezoid_cumulative,true_cumulative,trapezoid_absolute_error")
for i in 0:100
    t=i*h; r=rate(t)
    if i>0
        global left += rate((i-1)*h)*h
        global trap += 0.5*(rate((i-1)*h)+r)*h
    end
    truth=trueint(t)-trueint(0.0)
    println(join((i,t,r,left,trap,truth,abs(trap-truth)),","))
end
