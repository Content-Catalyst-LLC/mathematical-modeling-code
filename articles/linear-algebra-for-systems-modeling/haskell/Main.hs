module Main where

type Vector = [Double]
type Matrix = [[Double]]

matrixVector :: Matrix -> Vector -> Vector
matrixVector a x = map (sum . zipWith (*) x) a

state :: Vector
state = [100.0, 80.0, 60.0]

transition :: Matrix
transition =
  [ [0.90, 0.05, 0.00]
  , [0.10, 0.90, 0.10]
  , [0.00, 0.05, 0.90]
  ]

main :: IO ()
main = do
  putStrLn "Linear Algebra for Systems Modeling: typed matrix-vector transition"
  print (matrixVector transition state)
