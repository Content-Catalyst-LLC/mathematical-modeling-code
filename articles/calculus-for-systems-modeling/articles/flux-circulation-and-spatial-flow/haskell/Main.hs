module Main where

data Vec2 = Vec2 Double Double deriving (Show)

data FlowAudit = FlowAudit
  { scenario :: String
  , segmentCount :: Int
  , approximateFlux :: Double
  , approximateCirculation :: Double
  , meanTangentialAlignment :: Double
  , meanNormalAlignment :: Double
  , fieldDescription :: String
  , geometryDescription :: String
  , warning :: String
  } deriving (Show)

vectorField :: Double -> Double -> Vec2
vectorField x y = Vec2 (-y) x

dot :: Vec2 -> Vec2 -> Double
dot (Vec2 a b) (Vec2 c d) = a*c + b*d

norm :: Vec2 -> Double
norm v = sqrt (dot v v)

circlePoint :: Double -> Int -> Int -> Vec2
circlePoint radius segments i =
  let theta = 2 * pi * fromIntegral i / fromIntegral segments
  in Vec2 (radius * cos theta) (radius * sin theta)

auditCircleFlow :: Double -> Int -> String -> FlowAudit
auditCircleFlow radius segments label =
  let rows =
        [ let Vec2 x0 y0 = circlePoint radius segments i
              Vec2 x1 y1 = circlePoint radius segments (i + 1)
              xm = 0.5 * (x0 + x1)
              ym = 0.5 * (y0 + y1)
              dx = x1 - x0
              dy = y1 - y0
              segment = Vec2 dx dy
              segmentLength = norm segment
              tangent = Vec2 (dx / segmentLength) (dy / segmentLength)
              normal = Vec2 (xm / radius) (ym / radius)
              field = vectorField xm ym
          in (dot field normal * segmentLength, dot field segment, dot field tangent, dot field normal)
        | i <- [0 .. segments - 1] ]
      fluxes = [f | (f,_,_,_) <- rows]
      circulations = [c | (_,c,_,_) <- rows]
      tangents = [t | (_,_,t,_) <- rows]
      normals = [n | (_,_,_,n) <- rows]
      warningText =
        if segments < 32
        then "Coarse path sampling; circulation and flux should be checked with more segments."
        else "Synthetic flow audit; document field meaning, orientation, units, and boundary choice."
  in FlowAudit label segments (sum fluxes) (sum circulations) (sum tangents / fromIntegral segments) (sum normals / fromIntegral segments) "rotating field F=<-y,x>" ("counterclockwise circle with radius " ++ show radius) warningText

main :: IO ()
main = do
  print (auditCircleFlow 1.0 16 "coarse_circle")
  print (auditCircleFlow 1.0 64 "medium_circle")
  print (auditCircleFlow 1.0 256 "fine_circle")
