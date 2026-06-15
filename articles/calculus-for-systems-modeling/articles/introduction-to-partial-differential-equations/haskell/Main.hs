module Main where

data PDEGridRecord = PDEGridRecord
  { stepNumber :: Int
  , timeValue :: Double
  , centerValue :: Double
  , totalMass :: Double
  , maxValue :: Double
  , minValue :: Double
  , stabilityRatio :: Double
  , warning :: String
  } deriving (Show)

initializeField :: Int -> [Double]
initializeField n =
  [if i == div n 2 then 1.0 else 0.0 | i <- [0..n-1]]

diffusionStep :: Double -> [Double] -> [Double]
diffusionStep ratio field =
  zipWith update [0..] field
  where
    n = length field
    update i x
      | i == 0 = 0.0
      | i == n - 1 = 0.0
      | otherwise = x + ratio * ((field !! (i + 1)) - 2 * x + (field !! (i - 1)))

simulateDiffusion :: Int -> Double -> Double -> Double -> Int -> [PDEGridRecord]
simulateDiffusion gridPoints diffusivity dx dt steps =
  go 0 (initializeField gridPoints)
  where
    ratio = diffusivity * dt / (dx * dx)
    centerIndex = div gridPoints 2
    go step field
      | step > steps = []
      | otherwise =
          let record = PDEGridRecord
                step
                (fromIntegral step * dt)
                (field !! centerIndex)
                (sum field * dx)
                (maximum field)
                (minimum field)
                ratio
                "Explicit diffusion schemes require stability checks; boundary and grid assumptions shape results."
          in record : go (step + 1) (diffusionStep ratio field)

main :: IO ()
main =
  mapM_ print (simulateDiffusion 51 0.1 1.0 0.25 100)
