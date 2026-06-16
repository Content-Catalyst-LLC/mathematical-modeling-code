module Main where
initializeField n = [if i == div n 2 then 1.0 else 0.0 | i <- [0..n-1]]
main = mapM_ print (take 10 (initializeField 61))
