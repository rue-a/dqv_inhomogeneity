# Inhomogeneity in Data Quality - A Profile for DQV

_Currently, this repository is in the works. Feel free to browse around anyway._

This repository accompanies the shortpaper __Modelling Inhomogeneous Geodata Quality in a Dataset's Metadata__ [//link]. Please refer to this publication for a comprehensive description and the rational behind the profile.

DQV (Data Quality Vocabulary): <https://www.w3.org/TR/vocab-dqv/>

---

__Aim:__ Account for inhomogeneous data quality in a dataset's metadata; i.e. describing geodata quality at sub-dataset-level.

__Solution:__ Enable a DQV quality measurement to be assigned with a spatial, temporal and or thematical constraint that restricts its validity accordingly.

The profile can be implemented in two ways. Either by defining a node that describes the constraints and that is subsequently attached to the measurement node (version 1) or adding the spatial, temporal and thematic constraints to the measurement node directly (version 2). In the publication we argue that version 2 is currently more feasible. The differences in the two approaches are highlighted in `listing1_implementation_versions.ttl`. The profile does not change anything in the default version of DQV, it just adds triples. These triples can be found in the file `profile.ttl` in the folders `version_1` or `version_2` respectively.

## Contents (Selection)

`listing1_implementation_versions.ttl`: highlights differences between both versions.

`version_1/profile.ttl`: additions to DQV when using version 1.

`version_1/examples.ttl`: some examples that show how version 1 is used.

`version_2/profile.ttl`: additions to DQV when using version 2.

`version_2/examples.ttl`: some examples that show how version 2 is used.

`version_2/global_forest_change.ttl`: comprehensive example of application of profile in version 2. The file contains the metadata for the dataset *Global Forest Change* (Hansen et al., 2013; https://www.science.org/doi/10.1126/science.1244693). The data quality information is originally provided in the supplementary material in the form of text and tables; where it is disaggregated into different spatial, temporal and thematic scopes, e.g., error of forest loss from 2000 to 2012 in the tropical climate domain (https://www.science.org/doi/suppl/10.1126/science.1244693/suppl_file/hansen.sm.pdf, p. 17).

The example exposes the provided data quality information as queryable metadata.

`gez_2010_geometries`: The folder contains the geometries of the Global Ecological Zones as defined by FAO in 2010 (available at: https://data.apps.fao.org/map/catalog/srv/eng/catalog.search#/metadata/2fb209d0-fd34-4e5e-a3d8-a13c241eb61b). The geometries are converted with `geometries2GeoSPARQL_wkt_ttl.py`.

`quality_register`: contains descriptions of geodata quality indicators in DQV. SPARQL endpoint at: <https://geokur-dmp2.geo.tu-dresden.de/fuseki/geokur_quality_register/sparql>. See also: <https://geokur-dmp.geo.tu-dresden.de/quality-register>.


## Literature 

Hansen,   M.   C.,   Potapov,   P.   V.,   Moore,   R.,   Hancher,   M.,Turubanova,   S.   A.,   Tyukavina,   A.,   Thau,   D.,   Stehman,S.   V.,   Goetz,   S.   J.,   Loveland,   T.   R.,   Kommareddy,A.,   Egorov,   A.,   Chini,   L.,   Justice,   C.   O.,   and   Town-shend,  J.  R.  G.:  High-Resolution  Global  Maps  of  21st-Century   Forest   Cover   Change,   Science,   342,   850–853,https://doi.org/10.1126/science.1244693, 2013.

