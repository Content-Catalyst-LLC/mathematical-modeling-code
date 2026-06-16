module Main where

data DifferentiationRecord = DifferentiationRecord
  { indexValue :: Int
  , xValue :: Double
  , functionValue :: Double
  , trueDerivativeValue :: Double
  , centralDifferenceValue :: Maybe Double
  , centralAbsoluteError :: Maybe Double
  , stepSize :: Double
  , warning :: String
  } deriving (Show)

signal :: Double -> Double
signal x = sin x + 0.1 * x * x

trueDerivative :: Double -> Double
trueDerivative x = cos x + 0.2 * x

centralDifference :: [Double] -> Int -> Double -> Maybe Double
centralDifference values i h
  | i <= 0 = Nothing
  | i >= length values - 1 = Nothing
  | otherwise = Just (((values !! (i + 1)) - (values !! (i - 1))) / (2 * h))

buildRecords :: Double -> Double -> Double -> [DifferentiationRecord]
buildRecords start stop h =
  map build [0..n]
  where
    n = round ((stop - start) / h)
    xs = [start + fromIntegral i * h | i <- [0..n]]
    values = map signal xs

    build i =
      let x = xs !! i
          cd = centralDifference values i h
          err = fmap (\d -> abs (d - trueDerivative x)) cd
      in DifferentiationRecord
          i
          x
          (signal x)
          (trueDerivative x)
          cd
          err
          h
          "Numerical derivatives depend on step size, formula choice, boundary handling, smoothness, and noise."

main :: IO ()
main =
  mapM_ print (buildRecords 0.0 10.0 0.1)
