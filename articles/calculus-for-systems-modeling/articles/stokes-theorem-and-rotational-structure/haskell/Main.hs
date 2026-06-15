module Main where

data Vec3 = Vec3 Double Double Double deriving (Show)

data StokesAudit = StokesAudit
  { scenario :: String
  , radius :: Double
  , boundarySegments :: Int
  , radialSteps :: Int
  , boundaryCirculation :: Double
  , surfaceCurlFlux :: Double
  , absoluteGap :: Double
  , fieldDescription :: String
  , surfaceDescription :: String
  , orientationNote :: String
  , warning :: String
  } deriving (Show)

vectorField :: Double -> Double -> Double -> Vec3
vectorField x y _ = Vec3 (-y) x 0

curlField :: Double -> Double -> Double -> Vec3
curlField _ _ _ = Vec3 0 0 2

dot :: Vec3 -> Vec3 -> Double
dot (Vec3 a b c) (Vec3 d e f) = a*d + b*e + c*f

boundaryCirculationCircle :: Double -> Int -> Double
boundaryCirculationCircle radius segments =
  let contribution i =
        let theta0 = 2 * pi * fromIntegral i / fromIntegral segments
            theta1 = 2 * pi * fromIntegral (i + 1) / fromIntegral segments
            x0 = radius * cos theta0
            y0 = radius * sin theta0
            x1 = radius * cos theta1
            y1 = radius * sin theta1
            xm = 0.5 * (x0 + x1)
            ym = 0.5 * (y0 + y1)
            dx = x1 - x0
            dy = y1 - y0
        in dot (vectorField xm ym 0) (Vec3 dx dy 0)
  in sum [ contribution i | i <- [0 .. segments - 1] ]

surfaceCurlFluxDisk :: Double -> Int -> Double
surfaceCurlFluxDisk radius radialSteps =
  let normal = Vec3 0 0 1
      contribution i =
        let r0 = radius * fromIntegral i / fromIntegral radialSteps
            r1 = radius * fromIntegral (i + 1) / fromIntegral radialSteps
            ringArea = pi * (r1*r1 - r0*r0)
            rm = 0.5 * (r0 + r1)
        in dot (curlField rm 0 0) normal * ringArea
  in sum [ contribution i | i <- [0 .. radialSteps - 1] ]

auditStokes :: Double -> Int -> Int -> String -> StokesAudit
auditStokes radius segments radialSteps label =
  let circulation = boundaryCirculationCircle radius segments
      curlFlux = surfaceCurlFluxDisk radius radialSteps
      gap = abs (circulation - curlFlux)
      warningText =
        if segments < 64 || radialSteps < 16
        then "Coarse boundary or surface sampling; refine before interpreting the theorem comparison."
        else "Synthetic Stokes theorem audit; document field, surface, boundary, orientation, units, and numerical method."
  in StokesAudit label radius segments radialSteps circulation curlFlux gap "F=<-y,x,0>; curl F=<0,0,2>" "horizontal disk with upward normal" "counterclockwise boundary orientation viewed from positive z" warningText

main :: IO ()
main = do
  print (auditStokes 1.0 32 8 "coarse_audit")
  print (auditStokes 1.0 128 32 "medium_audit")
  print (auditStokes 1.0 512 128 "fine_audit")
