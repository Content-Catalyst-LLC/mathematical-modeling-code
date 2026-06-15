module Main where

data Point = Point Double Double deriving (Show)
data Vector = Vector Double Double deriving (Show)
data GridSpec = GridSpec Double deriving (Show)

data FieldAudit = FieldAudit
  { scenario :: String
  , gridStep :: Double
  , pointCount :: Int
  , scalarAverage :: Double
  , scalarMinimum :: Double
  , scalarMaximum :: Double
  , vectorMagnitudeAverage :: Double
  , vectorMagnitudeMaximum :: Double
  , domainDescription :: String
  , warning :: String
  } deriving (Show)

scalarField :: Point -> Double
scalarField (Point x y) =
  20.0 + 2.0 * sin x + 0.5 * y * y

vectorField :: Point -> Vector
vectorField (Point x y) =
  Vector (-y) x

vectorMagnitude :: Vector -> Double
vectorMagnitude (Vector vx vy) =
  sqrt (vx * vx + vy * vy)

gridValues :: Double -> [Double]
gridValues step =
  [ -3.0 + fromIntegral i * step | i <- [0 .. floor (6.0 / step)] ]

avg :: [Double] -> Double
avg values = sum values / fromIntegral (length values)

auditField :: GridSpec -> String -> FieldAudit
auditField (GridSpec step) label =
  let xs = gridValues step
      ys = gridValues step
      points = [ Point x y | x <- xs, y <- ys ]
      scalars = map scalarField points
      magnitudes = map (vectorMagnitude . vectorField) points
      warningText =
        if step > 0.75
        then "Grid resolution is coarse; field structure may be undersampled."
        else "Synthetic field audit; document domain, units, and interpolation assumptions."
  in FieldAudit
      label
      step
      (length points)
      (avg scalars)
      (minimum scalars)
      (maximum scalars)
      (avg magnitudes)
      (maximum magnitudes)
      "square domain [-3,3] x [-3,3]"
      warningText

main :: IO ()
main = do
  print (auditField (GridSpec 1.0) "coarse_grid")
  print (auditField (GridSpec 0.5) "medium_grid")
  print (auditField (GridSpec 0.25) "fine_grid")
