module Main where
data NetworkAdjacencyAudit = NetworkAdjacencyAudit String Int Int Bool Bool Double Double Double String deriving (Show)
main :: IO ()
main = print (NetworkAdjacencyAudit "synthetic_infrastructure_dependency_network" 5 20 True True 0.8 2.15 1.95 "Adjacency conclusions depend on node boundaries, edge definitions, direction conventions, weights, missing edges, and provenance.")
