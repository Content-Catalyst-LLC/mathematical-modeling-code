module Main where
rate t = 2.0 + sin t + 0.1*t
main = mapM_ print [(i, t, rate t) | i <- [0..100], let t = fromIntegral i * 0.1]
