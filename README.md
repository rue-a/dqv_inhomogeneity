# Inhomogeneity in Data Quality - A Profile for DQV

_Currently, this repository is in the works. Feel free to browse around anyway._

This repository accompanies the shortpaper __Modelling Inhomogeneous Geodata Quality in a Dataset's Metadata__ [//link]. Please refer to this publication for a comprehensive description and the rational behind the profile.

---

__Aim:__ Account for inhomogeneous data quality in a dataset's metadata; i.e. describing geodata quality at sub-dataset-level.

__Solution:__ Enable a DQV quality measurement to be assigned with a spatial, temporal and or thematical constraint that restricts its validity accordingly.

The profile can be implemented in two ways. Either by defining a node that describes the constraints and that is subsequently attached to the measurement node (version 1) or adding the spatial, temporal and thematic constraints to the measurement node directly (version 2). In the publication we argues that version 2 is currently more feasible. The differences in the two approaches are highlighted in `listing1_implementation_versions.ttl`.

## Summary of Contents (Selection)
