module Main where

data PolarSpec = PolarSpec Double Double Double deriving (Show)
data Audit = Audit
  { scenario :: String
  , radius :: Double
  , radialStep :: Double
  , angularStep :: Double
  , polarTotalValue :: Double
  , cartesianTotalValue :: Double
  , absoluteDifference :: Double
  , relativeDifference :: Double
  , jacobianRule :: String
  , warning :: String
  } deriving (Show)

exposureCartesian :: Double -> Double -> Double
exposureCartesian x y =
  let r = sqrt (x * x + y * y)
  in 20.0 * exp (-0.4 * r)

exposurePolar :: Double -> Double -> Double
exposurePolar r _ = 20.0 * exp (-0.4 * r)

polarTotal :: PolarSpec -> Double
polarTotal (PolarSpec radius dr dtheta) =
  let rs = takeWhile (< radius) [dr / 2.0, dr / 2.0 + dr ..]
      thetas = takeWhile (< 2.0 * pi) [dtheta / 2.0, dtheta / 2.0 + dtheta ..]
  in sum [ exposurePolar r theta * r * dr * dtheta | r <- rs, theta <- thetas ]

cartesianGridTotal :: Double -> Double -> Double
cartesianGridTotal radius step =
  let coords = [ -radius, -radius + step .. radius ]
      inside x y = x * x + y * y <= radius * radius
  in sum [ exposureCartesian x y * step * step | x <- coords, y <- coords, inside x y ]

audit :: PolarSpec -> String -> Audit
audit spec@(PolarSpec radius dr dtheta) label =
  let pTotal = polarTotal spec
      cTotal = cartesianGridTotal radius dr
      diff = abs (pTotal - cTotal)
      relDiff = diff / max (abs pTotal) 1.0e-12
      warningText =
        if dr > 0.5
        then "Resolution is coarse; transformed and Cartesian approximations may differ."
        else "Polar Jacobian factor r included; compare domain and resolution assumptions."
  in Audit label radius dr dtheta pTotal cTotal diff relDiff "dA = r dr dtheta" warningText

main :: IO ()
main = do
  print (audit (PolarSpec 3.0 0.5 (pi / 24.0)) "medium_polar_grid")
  print (audit (PolarSpec 3.0 0.25 (pi / 48.0)) "fine_polar_grid")
  print (audit (PolarSpec 3.0 0.125 (pi / 96.0)) "very_fine_polar_grid")
