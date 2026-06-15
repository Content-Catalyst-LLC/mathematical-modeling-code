module Main where

data Point = Point Double Double deriving (Show)

data TrajectoryAudit = TrajectoryAudit
  { scenario :: String
  , timeStep :: Double
  , pointCount :: Int
  , approximateArcLength :: Double
  , displacementMagnitude :: Double
  , pathEfficiency :: Double
  , averageSpeed :: Double
  , maximumSpeed :: Double
  , domainDescription :: String
  , warning :: String
  } deriving (Show)

position :: Double -> Point
position t = Point t (sin t)

distanceBetween :: Point -> Point -> Double
distanceBetween (Point x1 y1) (Point x2 y2) =
  sqrt ((x2 - x1) ^ 2 + (y2 - y1) ^ 2)

sampleTimes :: Double -> Double -> Double -> [Double]
sampleTimes start stop step =
  takeWhile (<= stop + 1.0e-9) [start, start + step ..]

pairwise :: [a] -> [(a,a)]
pairwise xs = zip xs (tail xs)

auditTrajectory :: Double -> String -> TrajectoryAudit
auditTrajectory step label =
  let times = sampleTimes 0.0 (2.0 * pi) step
      points = map position times
      segments = map (uncurry distanceBetween) (pairwise points)
      timeSteps = map (\(a,b) -> b - a) (pairwise times)
      speeds = zipWith (/) segments timeSteps
      arcLength = sum segments
      displacement = distanceBetween (head points) (last points)
      efficiency = displacement / max arcLength 1.0e-12
      warningText =
        if step > 0.5
        then "Time step is coarse; turns and speed variation may be undersampled."
        else "Synthetic trajectory audit; document units, parameter meaning, and sampling."
  in TrajectoryAudit label step (length points) arcLength displacement efficiency (sum speeds / fromIntegral (length speeds)) (maximum speeds) "trajectory r(t) = <t, sin(t)> for 0 <= t <= 2pi" warningText

main :: IO ()
main = do
  print (auditTrajectory 1.0 "coarse_time_step")
  print (auditTrajectory 0.5 "medium_time_step")
  print (auditTrajectory 0.25 "fine_time_step")
