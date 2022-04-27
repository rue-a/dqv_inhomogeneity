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

`version_2/global_forest_change.ttl`: comprehensive example of application of profile in version 2. The file contains the metadata for the dataset _Global Forest Change_ (Hansen et al., 2013; <https://www.science.org/doi/10.1126/science.1244693>). The data quality information is originally provided in the supplementary material in the form of text and tables; where it is disaggregated into different spatial, temporal and thematic scopes, e.g., error of forest loss from 2000 to 2012 in the tropical climate domain (<https://www.science.org/doi/suppl/10.1126/science.1244693/suppl_file/hansen.sm.pdf>, p. 17).

The example exposes the provided data quality information as queryable metadata.

`gez_2010_geometries`: The folder contains the geometries of the Global Ecological Zones as defined by FAO in 2010 (available at: <https://data.apps.fao.org/map/catalog/srv/eng/catalog.search#/metadata/2fb209d0-fd34-4e5e-a3d8-a13c241eb61b>). The geometries are converted with `geometries2GeoSPARQL_wkt_ttl.py`.

`quality_register`: contains descriptions of geodata quality indicators in DQV. SPARQL endpoint at: <https://geokur-dmp2.geo.tu-dresden.de/fuseki/geokur_quality_register/sparql>. See also: <https://geokur-dmp.geo.tu-dresden.de/quality-register>.

## Application Example

The Global Forest Change dataset contains metadata that describes the dataset's quality dataset-wide, as well as spatially, temporally and thematically disaggregated (see Contents). Without this extension, in a data catalog environment, only the dataset-wide quality information can be included in queries; e.g., Select datasets where the producers's accuracy is higher than 70 %. With this extension, the query can be much more specific: Select datasets where the producer's accuracy of forest gain (theme) in an area that intersects the bounding box of Columbia (spatial) is higher than 70 %. The dataset-wide producer's accuracy of forest gain is higher than 70 %, so the dataset would be selected in the first case, although, the producer's accuracy of forest gain in the tropical domain is lower than 70 % (it is 48 %). The according query (that uses the profile) is as follows. It is assumed that the thematic concept of forest gain is defined and accessible in the Linked Data cloud.

```SPARQL
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dqv: <http://www.w3.org/ns/dqv#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX gsp: <http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX gkq: <https://geokur-dmp.geo.tu-dresden.de/quality-register#>
PREFIX gez2010_geoms: <https://github.com/rue-a/dqv_inhomogeneity/blob/master/gaez_2010_geometries/>
PREFIX profile: <https://ex.org/profile/#> 
PREFIX : <https://ex.org/#>

SELECT DISTINCT ?dataset_title ?quality_indicator_label ?quality_extent_label ?prod_acc_val ?quality_theme_label ?quality_indicator_def ?quality_extent_def ?quality_theme_def
WHERE {
    ?dataset dqv:hasQualityMeasurement ?quality_measurement.
    ?quality_measurement dqv:isMeasurementOf gkq:ProducersAccuracy .
  	?quality_measurement dqv:value ?prod_acc_val .
    ?quality_measurement dct:spatial ?quality_extent .
    ?quality_extent gsp:hasDefaultGeometry ?extent_geom.
    ?extent_geom gsp:asWKT ?extent_wkt .
    BIND("POLYGON((-78.9909352282 -4.298186944190007,-78.9909352282 12.437303168200003,-66.8763258531 12.437303168200003,-66.8763258531 -4.298186944190007,-78.9909352282 -4.298186944190007))"^^gsp:wktLiteral AS ?bbox_columbia_wkt)
    BIND("70"^^xsd:double AS ?threshold)
    BIND(:forestGain AS ?quality_theme)
    ?quality_measurement profile:thematic ?quality_theme .
    FILTER(?prod_acc_val > ?threshold && geof:sfIntersects(?bbox_columbia_wkt, ?extent_wkt))
    
    ?dataset dct:title ?dataset_title . 
    gkq:ProducersAccuracy skos:prefLabel ?quality_indicator_label .
    gkq:ProducersAccuracy skos:definition ?quality_indicator_def .    
    ?quality_theme skos:prefLabel ?quality_theme_label .
    ?quality_theme skos:definition ?quality_theme_def .
    ?quality_extent skos:prefLabel ?quality_extent_label .
    ?quality_extent skos:definition ?quality_extent_def .
}
```

To test this query, you can download [jena-fuseki-geosparql (4.4.0)](https://repo1.maven.org/maven2/org/apache/jena/jena-fuseki-geosparql/4.4.0/jena-fuseki-geosparql-4.4.0.jar), which lets you set up a local GeoSPARQL-ready triplestore. Run the command `java -jar jena-fuseki-geosparql-4.4.0.jar -rf ".\version_2\global_forest_change.ttl,.\version_2\profile.ttl,.\gez_2010_geometries\polar.ttl,.\gez_2010_geometries\boreal.ttl,.\gez_2010_geometries\temperate.ttl,.\gez_2010_geometries\subtropical.ttl,.\gez_2010_geometries\tropical.ttl,.\gez_2010_geometries\water.ttl,.\quality_register.ttl" -i -v -d global_forest_change_example` in this repository's folder. That sets up a queryable triplestore at http://localhost:3030/global_forest_change_example/sparql. If you execute the query against the triplestore you won't get any results, since there is no dataset that has a producer's accuracy higher than 70 % for forest gain in the area of Columbia. You have to reduce the `?threshold` value to find a dataset. Try setting it to 40 to get:

    "dataset_title": "Global Forest Change"

    "quality_indicator_label": "Producer's Accuracy"

    "quality_extent_label": "Tropical Ecological Zone 2010"

    "prod_acc_val": "48.0"

    "quality_theme_label": "Forest Gain"

    "quality_indicator_def": "Producer's accuracy looks at accuracy from the perspective of the creator of a land cover data set. It corresponds to the statistical concept of errors of omission - in other words, inadvertent exclusion from a given category.  Producer's accuracy indicates for a given class the proportion of the reference data that are classified correctly.  It is calculated as the number of pixels in a given class divided by the number of pixels in the reference data in that class.  Assuming that an error matrix is organised with the reference data in columns, producer's accuracy is therefore calculated by looking at column totals (<https://www2.geog.soton.ac.uk/users/trevesr/obs/rseo/accuracy_assessment__error_matrices.html>; 25.01.2022)"

    "quality_extent_def": "All months without frost: in marine areas over 18°C"

    "quality_theme_def": "\"Forest gain was defined as the inverse of loss, or the establishment of tree canopy from a nonforest state.\" [https://www.science.org/doi/epdf/10.1126/science.1244693]"




## Literature

Hansen, M. C., Potapov, P. V., Moore, R., Hancher, M.,Turubanova, S. A., Tyukavina, A., Thau, D., Stehman,S. V., Goetz, S. J., Loveland, T. R., Kommareddy,A., Egorov, A., Chini, L., Justice, C. O., and Townshend, J. R. G.: High-Resolution Global Maps of 21st-Century Forest Cover Change, Science, 342, 850–853,<https://doi.org/10.1126/science.1244693>, 2013.
