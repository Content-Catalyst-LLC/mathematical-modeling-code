module Main where

data Vec2 = Vec2 Double Double deriving (Show)

data FieldOperatorAudit = FieldOperatorAudit
  { scenario :: String
  , gridStep :: Double
  , pointCount :: Int
  , meanGradientMagnitude :: Double
  , maximumGradientMagnitude :: Double
  , meanDivergence :: Double
  , meanCurl :: Double
  , maximumAbsCurl :: Double
  , fieldDescription :: String
  , warning :: String
  } deriving (Show)

scalarField :: Double -> Double -> Double
scalarField x y = x*x + y*y

vectorField :: Double -> Double -> Vec2
vectorField x y = Vec2 (-y) x

gradientField :: Double -> Double -> Vec2
gradientField x y = Vec2 (2*x) (2*y)

divergenceField :: Double -> Double -> Double
divergenceField _ _ = 0.0

curl2D :: Double -> Double -> Double
curl2D _ _ = 2.0

vecNorm :: Vec2 -> Double
vecNorm (Vec2 a b) = sqrt (a*a + b*b)

gridValues :: Double -> [Double]
gridValues step = [ -1.0 + fromIntegral i * step | i <- [0 .. floor (2.0 / step)] ]

auditFieldOperators :: Double -> String -> FieldOperatorAudit
auditFieldOperators step label =
  let values = gridValues step
      points = [ (x,y) | x <- values, y <- values ]
      gradMagnitudes = [ vecNorm (gradientField x y) | (x,y) <- points ]
      divergences = [ divergenceField x y | (x,y) <- points ]
      curls = [ curl2D x y | (x,y) <- points ]
      warningText =
        if step > 0.5
        then "Grid step is coarse; local derivative structure may be undersampled."
        else "Synthetic field-operator audit; document field definitions, units, grid, and boundary rules."
  in FieldOperatorAudit
      label
      step
      (length points)
      (sum gradMagnitudes / fromIntegral (length gradMagnitudes))
      (maximum gradMagnitudes)
      (sum divergences / fromIntegral (length divergences))
      (sum curls / fromIntegral (length curls))
      (maximum (map abs curls))
      "scalar f=x^2+y^2; vector F=<-y,x>"
      warningText

main :: IO ()
main = do
  print (auditFieldOperators 1.0 "coarse_grid")
  print (auditFieldOperators 0.5 "medium_grid")
  print (auditFieldOperators 0.25 "fine_grid")
