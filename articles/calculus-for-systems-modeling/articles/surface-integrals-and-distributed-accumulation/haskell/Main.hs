module Main where

data Vec3 = Vec3 Double Double Double deriving (Show)

data SurfaceIntegralAudit = SurfaceIntegralAudit
  { scenario :: String
  , gridStep :: Double
  , patchCount :: Int
  , approximateSurfaceArea :: Double
  , scalarSurfaceIntegral :: Double
  , vectorFluxIntegral :: Double
  , averageFluxDensity :: Double
  , maximumPatchArea :: Double
  , surfaceDescription :: String
  , warning :: String
  } deriving (Show)

height :: Double -> Double -> Double
height x y = 0.1 * x * x + 0.05 * y * y

scalarField :: Double -> Double -> Double -> Double
scalarField _ _ z = 1.0 + 0.2 * z

vectorField :: Double -> Double -> Double -> Vec3
vectorField x y _ = Vec3 (0.1 * x) (0.1 * y) 1.0

normalAreaVector :: Double -> Double -> Double -> Vec3
normalAreaVector x y step =
  let dzdx = 0.2 * x
      dzdy = 0.1 * y
      area = step * step
  in Vec3 (-dzdx * area) (-dzdy * area) area

dot :: Vec3 -> Vec3 -> Double
dot (Vec3 a b c) (Vec3 d e f) = a*d + b*e + c*f

norm :: Vec3 -> Double
norm v = sqrt (dot v v)

gridValues :: Double -> [Double]
gridValues step = [ -1.0 + fromIntegral i * step | i <- [0 .. floor (2.0 / step) - 1] ]

auditSurface :: Double -> String -> SurfaceIntegralAudit
auditSurface step label =
  let xs = gridValues step
      ys = gridValues step
      patches = [ (x,y) | x <- xs, y <- ys ]
      patchRows =
        [ let z = height x y
              areaVector = normalAreaVector x y step
              patchArea = norm areaVector
              scalarValue = scalarField x y z
              flux = dot (vectorField x y z) areaVector
          in (patchArea, scalarValue * patchArea, flux, flux / max patchArea 1.0e-12)
        | (x,y) <- patches ]
      patchAreas = [a | (a,_,_,_) <- patchRows]
      scalarTerms = [s | (_,s,_,_) <- patchRows]
      fluxTerms = [f | (_,_,f,_) <- patchRows]
      fluxDensities = [d | (_,_,_,d) <- patchRows]
      warningText =
        if step > 0.5
        then "Grid step is coarse; curvature and field variation may be undersampled."
        else "Synthetic surface-integral audit; document surface, normal, units, and mesh."
  in SurfaceIntegralAudit
      label
      step
      (length patches)
      (sum patchAreas)
      (sum scalarTerms)
      (sum fluxTerms)
      (sum fluxDensities / fromIntegral (length fluxDensities))
      (maximum patchAreas)
      "graph z = 0.1x^2 + 0.05y^2 over [-1,1] x [-1,1]"
      warningText

main :: IO ()
main = do
  print (auditSurface 1.0 "coarse_surface_mesh")
  print (auditSurface 0.5 "medium_surface_mesh")
  print (auditSurface 0.25 "fine_surface_mesh")
