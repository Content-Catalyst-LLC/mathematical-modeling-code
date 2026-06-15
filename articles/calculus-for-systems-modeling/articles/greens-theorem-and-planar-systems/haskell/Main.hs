module Main where

data Vec2 = Vec2 Double Double deriving (Show)

data GreensAudit = GreensAudit
  { scenario :: String
  , boundarySegmentsPerSide :: Int
  , interiorGridStep :: Double
  , boundaryCirculation :: Double
  , interiorCurlIntegral :: Double
  , boundaryFlux :: Double
  , interiorDivergenceIntegral :: Double
  , circulationGap :: Double
  , fluxGap :: Double
  , fieldDescription :: String
  , regionDescription :: String
  , warning :: String
  } deriving (Show)

rotationField :: Double -> Double -> Vec2
rotationField x y = Vec2 (-y) x

expansionField :: Double -> Double -> Vec2
expansionField x y = Vec2 x y

planarCurl :: Double -> Double -> Double
planarCurl _ _ = 2.0

planarDivergence :: Double -> Double -> Double
planarDivergence _ _ = 2.0

boundaryPoints :: Int -> [Vec2]
boundaryPoints n =
  let bottom = [Vec2 (-1 + 2 * fromIntegral i / fromIntegral n) (-1) | i <- [0..n-1]]
      rightSide = [Vec2 1 (-1 + 2 * fromIntegral i / fromIntegral n) | i <- [0..n-1]]
      topSide = [Vec2 (1 - 2 * fromIntegral i / fromIntegral n) 1 | i <- [0..n-1]]
      leftSide = [Vec2 (-1) (1 - 2 * fromIntegral i / fromIntegral n) | i <- [0..n-1]]
      pts = bottom ++ rightSide ++ topSide ++ leftSide
  in pts ++ [head pts]

boundaryCirculation :: Int -> Double
boundaryCirculation n =
  let pairs = zip (boundaryPoints n) (tail (boundaryPoints n))
      contribution (Vec2 x0 y0, Vec2 x1 y1) =
        let xm = 0.5 * (x0 + x1)
            ym = 0.5 * (y0 + y1)
            dx = x1 - x0
            dy = y1 - y0
            Vec2 p q = rotationField xm ym
        in p*dx + q*dy
  in sum (map contribution pairs)

boundaryFlux :: Int -> Double
boundaryFlux n =
  let pairs = zip (boundaryPoints n) (tail (boundaryPoints n))
      contribution (Vec2 x0 y0, Vec2 x1 y1) =
        let xm = 0.5 * (x0 + x1)
            ym = 0.5 * (y0 + y1)
            dx = x1 - x0
            dy = y1 - y0
            Vec2 p q = expansionField xm ym
        in p*dy + q*(-dx)
  in sum (map contribution pairs)

interiorIntegral :: Double -> (Double -> Double -> Double) -> Double
interiorIntegral step fn =
  let values = [ -1.0 + fromIntegral i * step | i <- [0 .. floor (2.0 / step) - 1] ]
      cells = [ (x + 0.5 * step, y + 0.5 * step) | x <- values, y <- values ]
  in sum [ fn x y * step * step | (x,y) <- cells ]

auditGreens :: Int -> Double -> String -> GreensAudit
auditGreens segments step label =
  let bc = boundaryCirculation segments
      ic = interiorIntegral step planarCurl
      bf = boundaryFlux segments
      idv = interiorIntegral step planarDivergence
      warningText =
        if segments < 16 || step > 0.25
        then "Coarse boundary or interior sampling; refine before interpreting the theorem comparison."
        else "Synthetic Green's theorem audit; document field, region, orientation, units, and numerical method."
  in GreensAudit label segments step bc ic bf idv (abs (bc-ic)) (abs (bf-idv)) "circulation F=<-y,x>; flux G=<x,y>" "positively oriented square [-1,1] x [-1,1]" warningText

main :: IO ()
main = do
  print (auditGreens 8 0.5 "coarse_audit")
  print (auditGreens 32 0.25 "medium_audit")
  print (auditGreens 128 0.125 "fine_audit")
