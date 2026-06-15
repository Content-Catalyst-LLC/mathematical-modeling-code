module Main where

newtype Time = Time Double deriving (Show)
newtype Height = Height Double deriving (Show)
newtype Volume = Volume Double deriving (Show)
newtype Rate = Rate Double deriving (Show)
newtype Sensitivity = Sensitivity Double deriving (Show)

data RelatedRateAudit = RelatedRateAudit
  { time :: Time
  , heightValue :: Height
  , heightRateValue :: Rate
  , volumeValue :: Volume
  , structuralDerivative :: Sensitivity
  , inferredVolumeRate :: Rate
  , warning :: String
  } deriving (Show)

volume :: Height -> Double
volume (Height h) = 12.0 * h * h

dVolumeDHeight :: Height -> Double
dVolumeDHeight (Height h) = 24.0 * h

heightPath :: Time -> Double
heightPath (Time t) = 2.0 + 0.08 * t

heightRate :: Time -> Double
heightRate _ = 0.08

auditTime :: Time -> RelatedRateAudit
auditTime t =
  let hValue = heightPath t
      h = Height hValue
      hRate = heightRate t
      v = volume h
      structural = dVolumeDHeight h
      vRate = structural * hRate
      warningText = if hValue <= 0.0 then "height outside physical domain" else ""
  in RelatedRateAudit t h (Rate hRate) (Volume v) (Sensitivity structural) (Rate vRate) warningText

main :: IO ()
main = mapM_ (print . auditTime . Time) [0.0, 5.0, 10.0, 20.0, 40.0]
