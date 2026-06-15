module Main where

data ChaosRecord = ChaosRecord
  { stepNumber :: Int
  , xReference :: Double
  , xPerturbed :: Double
  , absoluteDifference :: Double
  , warning :: String
  } deriving (Show)

logisticMap :: Double -> Double -> Double
logisticMap r x =
  r * x * (1 - x)

buildRecords :: Double -> Double -> Double -> Int -> [ChaosRecord]
buildRecords x0 perturbation r steps =
  take (steps + 1) $
    zipWith makeRecord [0..] referenceSeries
  where
    referenceSeries = iterate (logisticMap r) x0
    perturbedSeries = iterate (logisticMap r) (x0 + perturbation)
    makeRecord i x =
      let y = perturbedSeries !! i
      in ChaosRecord
          i
          x
          y
          (abs (x - y))
          "Trajectory divergence depends on parameter value, initial uncertainty, numerical precision, and iteration count."

main :: IO ()
main =
  mapM_ print (buildRecords 0.2 1e-8 3.9 30)
