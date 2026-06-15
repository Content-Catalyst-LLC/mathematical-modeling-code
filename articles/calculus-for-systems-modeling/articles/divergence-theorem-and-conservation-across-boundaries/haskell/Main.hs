module Main where

data Vec3 = Vec3 Double Double Double deriving (Show)

data DivergenceAudit = DivergenceAudit
  { scenario :: String
  , gridSteps :: Int
  , boundaryFlux :: Double
  , volumeDivergenceIntegral :: Double
  , absoluteGap :: Double
  , fieldDescription :: String
  , volumeDescription :: String
  , normalNote :: String
  , warning :: String
  } deriving (Show)

vectorField :: Double -> Double -> Double -> Vec3
vectorField x y z = Vec3 x y z

divergence :: Double -> Double -> Double -> Double
divergence _ _ _ = 3.0

boundaryFluxUnitCube :: Int -> Double
boundaryFluxUnitCube n =
  let step = 1.0 / fromIntegral n
      area = step * step
      indices = [0 .. n - 1]
      faceContribution i j =
        let y = (fromIntegral i + 0.5) * step
            z = (fromIntegral j + 0.5) * step
            x = (fromIntegral i + 0.5) * step
            y2 = (fromIntegral j + 0.5) * step
            Vec3 fx0 _ _ = vectorField 0 y z
            Vec3 fx1 _ _ = vectorField 1 y z
            Vec3 _ fy0 _ = vectorField x 0 z
            Vec3 _ fy1 _ = vectorField x 1 z
            Vec3 _ _ fz0 = vectorField x y2 0
            Vec3 _ _ fz1 = vectorField x y2 1
        in area * (fx0 * (-1) + fx1 + fy0 * (-1) + fy1 + fz0 * (-1) + fz1)
  in sum [ faceContribution i j | i <- indices, j <- indices ]

volumeDivergenceUnitCube :: Int -> Double
volumeDivergenceUnitCube n =
  let step = 1.0 / fromIntegral n
      cellVolume = step ** 3
      indices = [0 .. n - 1]
      contribution i j k =
        let x = (fromIntegral i + 0.5) * step
            y = (fromIntegral j + 0.5) * step
            z = (fromIntegral k + 0.5) * step
        in divergence x y z * cellVolume
  in sum [ contribution i j k | i <- indices, j <- indices, k <- indices ]

auditDivergenceTheorem :: Int -> String -> DivergenceAudit
auditDivergenceTheorem n label =
  let flux = boundaryFluxUnitCube n
      divIntegral = volumeDivergenceUnitCube n
      gap = abs (flux - divIntegral)
      warningText =
        if n < 8
        then "Coarse grid; refine before interpreting the boundary-volume comparison."
        else "Synthetic divergence theorem audit; document field, volume, boundary, normals, units, and numerical method."
  in DivergenceAudit label n flux divIntegral gap "F=<x,y,z>; divergence = 3" "unit cube [0,1] x [0,1] x [0,1]" "all six cube faces use outward normals" warningText

main :: IO ()
main = do
  print (auditDivergenceTheorem 4 "coarse_audit")
  print (auditDivergenceTheorem 16 "medium_audit")
  print (auditDivergenceTheorem 64 "fine_audit")
