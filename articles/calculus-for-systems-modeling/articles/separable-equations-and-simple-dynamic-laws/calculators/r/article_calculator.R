args <- commandArgs(trailingOnly = TRUE); cmd <- args[[1]]; dir.create('outputs', showWarnings=FALSE)
get <- function(i,d) if(length(args)>=i) args[[i]] else d
write_result <- function(name,df){write.csv(df,file.path('outputs',paste0(name,'.csv')),row.names=FALSE);print(df)}
if(cmd=='exponential-solution'){t=as.numeric(get(2,'2'));x0=as.numeric(get(3,'10'));r=as.numeric(get(4,'0.25'));write_result('r_exponential_solution',data.frame(calculator=cmd,time=t,initial=x0,growth_rate=r,state=x0*exp(r*t)))}
else if(cmd=='exponential-rate'){x=as.numeric(get(2,'10'));r=as.numeric(get(3,'0.25'));write_result('r_exponential_rate',data.frame(calculator=cmd,state=x,growth_rate=r,rate=r*x))}
else if(cmd=='logistic-solution'){t=as.numeric(get(2,'2'));x0=as.numeric(get(3,'10'));r=as.numeric(get(4,'0.25'));k=as.numeric(get(5,'100'));write_result('r_logistic_solution',data.frame(calculator=cmd,time=t,initial=x0,growth_rate=r,capacity=k,state=k/(1+((k-x0)/x0)*exp(-r*t))))}
else if(cmd=='logistic-rate'){x=as.numeric(get(2,'10'));r=as.numeric(get(3,'0.25'));k=as.numeric(get(4,'100'));write_result('r_logistic_rate',data.frame(calculator=cmd,state=x,growth_rate=r,capacity=k,rate=r*x*(1-x/k)))}
else stop(paste('Unknown command:',cmd))
