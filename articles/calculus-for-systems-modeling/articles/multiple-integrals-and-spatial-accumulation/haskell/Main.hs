module Main where

data Point = Point Double Double deriving (Show)
data GridSpec = GridSpec Double deriving (Show)
data SpatialAudit = SpatialAudit
  { scenario :: String
  , cellsInRegion :: Int
  , cellArea :: Double
  , totalArea :: Double
  , totalDensityAccumulation :: Double
  , areaWeightedAverage :: Double
  , populationWeightedBurden :: Double
  , populationTotal :: Double
  , populationWeightedAverageExposure :: Double
  , warning :: String
  } deriving (Show)

exposureField :: Point -> Double
exposureField (Point x y) = 10.0 + 2.0 * x + 0.5 * y * y

populationDensity :: Point -> Double
populationDensity (Point x y) = 100.0 + 10.0 * y + 5.0 * sin x

inRegion :: Point -> Bool
inRegion (Point x y) = x * x + y * y <= 9.0

gridValues :: Double -> [Double]
gridValues step = [ -3.0 + fromIntegral i * step | i <- [0 .. floor (6.0 / step)] ]

computeSpatialAccumulation :: GridSpec -> String -> SpatialAudit
computeSpatialAccumulation (GridSpec step) label =
  let xs = gridValues step
      ys = gridValues step
      cell = step * step
      points = [ Point x y | x <- xs, y <- ys, inRegion (Point x y) ]
      cells = length points
      totalDensity = sum [ exposureField p * cell | p <- points ]
      totalPopulation = sum [ populationDensity p * cell | p <- points ]
      populationBurden = sum [ exposureField p * populationDensity p * cell | p <- points ]
      area = fromIntegral cells * cell
      areaAverage = totalDensity / area
      populationAverage = populationBurden / totalPopulation
      warningText =
        if step > 0.5
        then "Grid resolution is coarse; spatial accumulation may smooth local variation."
        else "Synthetic grid audit; region mask, cell area, and units should be documented."
  in SpatialAudit label cells cell area totalDensity areaAverage populationBurden totalPopulation populationAverage warningText

main :: IO ()
main = do
  print (computeSpatialAccumulation (GridSpec 1.0) "coarse_grid")
  print (computeSpatialAccumulation (GridSpec 0.5) "medium_grid")
  print (computeSpatialAccumulation (GridSpec 0.25) "fine_grid")
