module Main where

newtype Time = Time Double deriving (Show)
newtype Emissions = Emissions Double deriving (Show)
newtype Concentration = Concentration Double deriving (Show)
newtype Forcing = Forcing Double deriving (Show)
newtype Temperature = Temperature Double deriving (Show)
newtype Sensitivity = Sensitivity Double deriving (Show)

data ChainRuleAudit = ChainRuleAudit
  { time :: Time
  , emissionsValue :: Emissions
  , concentrationValue :: Concentration
  , forcingValue :: Forcing
  , temperatureValue :: Temperature
  , emissionsRateValue :: Sensitivity
  , concentrationSensitivity :: Sensitivity
  , forcingSensitivity :: Sensitivity
  , temperatureSensitivity :: Sensitivity
  , totalDerivative :: Sensitivity
  } deriving (Show)

emissions :: Time -> Double
emissions (Time t) = 50.0 * exp (0.015 * t)

emissionsRate :: Time -> Double
emissionsRate t = 0.015 * emissions t

concentration :: Emissions -> Double
concentration (Emissions e) = 0.5 * e

dConcentrationDEmissions :: Emissions -> Double
dConcentrationDEmissions _ = 0.5

forcing :: Concentration -> Double
forcing (Concentration c) = log (1.0 + c)

dForcingDConcentration :: Concentration -> Double
dForcingDConcentration (Concentration c) = 1.0 / (1.0 + c)

temperatureResponse :: Forcing -> Double
temperatureResponse (Forcing f) = 1.2 * f

dTemperatureDForcing :: Forcing -> Double
dTemperatureDForcing _ = 1.2

chainRuleAudit :: Time -> ChainRuleAudit
chainRuleAudit t =
  let e = emissions t
      c = concentration (Emissions e)
      f = forcing (Concentration c)
      temp = temperatureResponse (Forcing f)
      s1 = emissionsRate t
      s2 = dConcentrationDEmissions (Emissions e)
      s3 = dForcingDConcentration (Concentration c)
      s4 = dTemperatureDForcing (Forcing f)
      total = s4 * s3 * s2 * s1
  in ChainRuleAudit t (Emissions e) (Concentration c) (Forcing f) (Temperature temp) (Sensitivity s1) (Sensitivity s2) (Sensitivity s3) (Sensitivity s4) (Sensitivity total)

main :: IO ()
main = mapM_ (print . chainRuleAudit . Time) [0.0, 5.0, 10.0, 20.0, 40.0]
