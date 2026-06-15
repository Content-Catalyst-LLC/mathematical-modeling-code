module Main where

data SpatialAuditRecord = SpatialAuditRecord
  { stepNumber :: Int
  , timeValue :: Double
  , centerValue :: Double
  , totalMass :: Double
  , maxValue :: Double
  , minValue :: Double
  , diffusionRatio :: Double
  , transportRatio :: Double
  , warning :: String
  } deriving (Show)

initializeField :: Int -> [Double]
initializeField n =
  [if i == div n 2 then 1.0 else 0.0 | i <- [0..n-1]]

updateField :: Double -> Double -> [Double] -> [Double]
updateField dRatio tRatio field =
  zipWith update [0..] field
  where
    n = length field
    update i x
      | i == 0 = 0.0
      | i == n - 1 = 0.0
      | otherwise =
          let diffusionPart = dRatio * ((field !! (i + 1)) - 2 * x + (field !! (i - 1)))
              transportPart = -tRatio * (x - (field !! (i - 1)))
          in x + diffusionPart + transportPart

simulateSpatialDynamics :: Int -> Double -> Double -> Double -> Double -> Int -> [SpatialAuditRecord]
simulateSpatialDynamics gridPoints diffusivity velocity dx dt steps =
  go 0 (initializeField gridPoints)
  where
    dRatio = diffusivity * dt / (dx * dx)
    tRatio = velocity * dt / dx
    centerIndex = div gridPoints 2

    go step field
      | step > steps = []
      | otherwise =
          let record = SpatialAuditRecord
                step
                (fromIntegral step * dt)
                (field !! centerIndex)
                (sum field * dx)
                (maximum field)
                (minimum field)
                dRatio
                tRatio
                "Spatial dynamics depend on field meaning, boundary conditions, grid spacing, time step, and numerical stability."
          in record : go (step + 1) (updateField dRatio tRatio field)

main :: IO ()
main =
  mapM_ print (simulateSpatialDynamics 61 0.08 0.4 1.0 0.2 120)
