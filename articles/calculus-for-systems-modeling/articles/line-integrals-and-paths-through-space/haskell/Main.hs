module Main where

data Point = Point Double Double deriving (Show)
data Vector = Vector Double Double deriving (Show)

data LineIntegralAudit = LineIntegralAudit
  { scenario :: String
  , timeStep :: Double
  , pointCount :: Int
  , pathLength :: Double
  , scalarLineIntegral :: Double
  , vectorLineIntegral :: Double
  , averageAlignment :: Double
  , maximumSegmentLength :: Double
  , pathDescription :: String
  , warning :: String
  } deriving (Show)

pathPoint :: Double -> Point
pathPoint t = Point t (sin t)

scalarField :: Point -> Double
scalarField (Point _ y) = 1.0 + y * y

vectorField :: Point -> Vector
vectorField (Point x _) = Vector 1.0 x

distanceBetween :: Point -> Point -> Double
distanceBetween (Point x1 y1) (Point x2 y2) = sqrt ((x2 - x1) ^ 2 + (y2 - y1) ^ 2)

displacement :: Point -> Point -> Vector
displacement (Point x1 y1) (Point x2 y2) = Vector (x2 - x1) (y2 - y1)

dot :: Vector -> Vector -> Double
dot (Vector a b) (Vector c d) = a * c + b * d

sampleTimes :: Double -> Double -> Double -> [Double]
sampleTimes start stop step = takeWhile (<= stop + 1.0e-9) [start, start + step ..]

pairwise :: [a] -> [(a,a)]
pairwise xs = zip xs (tail xs)

auditLineIntegral :: Double -> String -> LineIntegralAudit
auditLineIntegral step label =
  let times = sampleTimes 0.0 (2.0 * pi) step
      points = map pathPoint times
      pairs = pairwise points
      segmentLengths = map (uncurry distanceBetween) pairs
      scalarTerms = [ scalarField p * distanceBetween p q | (p,q) <- pairs ]
      vectorTerms = [ dot (vectorField p) (displacement p q) | (p,q) <- pairs ]
      alignments = zipWith (/) vectorTerms (map (max 1.0e-12) segmentLengths)
      warningText = if step > 0.5 then "Time step is coarse; path turns and field variation may be undersampled." else "Synthetic line-integral audit; document path, field, units, and interpolation."
  in LineIntegralAudit label step (length points) (sum segmentLengths) (sum scalarTerms) (sum vectorTerms) (sum alignments / fromIntegral (length alignments)) (maximum segmentLengths) "path r(t) = <t, sin(t)> for 0 <= t <= 2pi" warningText

main :: IO ()
main = do
  print (auditLineIntegral 1.0 "coarse_path")
  print (auditLineIntegral 0.5 "medium_path")
  print (auditLineIntegral 0.25 "fine_path")
