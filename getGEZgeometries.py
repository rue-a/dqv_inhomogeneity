# %%
from rdflib.namespace import Namespace, RDF, XSD, SKOS, RDFS
from rdflib import Graph, Literal, RDF, URIRef, BNode
import rdflib
import geopandas
from geopandas import GeoSeries
# %%

# https://data.apps.fao.org/map/catalog/srv/eng/catalog.search#/metadata/2fb209d0-fd34-4e5e-a3d8-a13c241eb61b
gdf = geopandas.read_file('https://storage.googleapis.com/fao-maps-catalog-data/uuid/2fb209d0-fd34-4e5e-a3d8-a13c241eb61b/resources/gez2010.zip')

tropical = []
subtropical = []
temperate = []
boreal = []
polar = []
water = []


for index, row in gdf.iterrows():
    if 'Tropical' in row['gez_name']:
        tropical.append(row['geometry'])
    if 'Subtropical' in row['gez_name']:
        subtropical.append(row['geometry'])
    if 'Temperate' in row['gez_name']:
        temperate.append(row['geometry'])
    if 'Boreal' in row['gez_name']:
        boreal.append(row['geometry'])
    if 'Polar' in row['gez_name']:
        polar.append(row['geometry'])
    if 'Water' in row['gez_name']:
        water.append(row['geometry'])

tropical_polygon = GeoSeries(tropical).unary_union
subtropical_polygon = GeoSeries(subtropical).unary_union
temperate_polygon = GeoSeries(temperate).unary_union
boreal_polygon = GeoSeries(boreal).unary_union
polar_polygon = GeoSeries(polar).unary_union
water_polygon = GeoSeries(water).unary_union

# %%
gez_def = '''
Conventionally the Food and Agriculture Organization of the United Nations (FAO) reports forest statistics according to political divisions: Nations, Regions and Continents. Expert consultations to the FRA held in Kotka, Finland, provided a mandate for FAO to incorporate indicators of biodiversity into the Assessment (FAO, 2001). In response FAO developed the Global Ecological Zones (GEZ) classification and maps, which were used to present forest statistics including information on forest cover change. An Ecological Zone (EZ) is defined as:\n “A zone or area with broad yet relatively homogeneous natural vegetation formations, similar (not necessarily identical) in physiognomy. Boundaries of the EZs approximately coincide with the map of Köppen-Trewartha climatic types, which was based on temperature and rainfall. An exception to this definition are “Mountain systems”, classified as one separate EZ in each Domain and characterized by a high variation in both vegetation formations and climatic conditions caused by large altitude and topographic variation” [Simons, H. (2001) FRA 2000. Global Ecological Zoning for the Global Forest Resources Assessment 2000. FRA Working Paper 56. FAO, Rome.] [https://www.fao.org/3/ap861e/ap861e.pdf].
'''
gez2010_def = '''
The GEZ spatial dataset used by FAO has developed over the years from covering only the tropical areas (1990) to the globe (2000). Due to the developments in remote sensing and the compiling of many spatial products relating to climate and land cover between 2000 and 2010, an update to the GEZ 2000 map was commissioned. This took the form of two months’ consultant work spread over ay-August 2011, and contributions from other scientists, particularly for North America and Australia. [https://www.fao.org/3/ap861e/ap861e.pdf]
'''

DCT = Namespace("http://purl.org/dc/terms/")
GKQ = Namespace('https://geokur-dmp.geo.tu-dresden.de/quality-register#')
GSP = Namespace('http://www.opengis.net/ont/geosparql#')
PROFILE = Namespace('https://ex.org/profile/#')
EX = Namespace('https://ex.org/#')
FAO = Namespace('https://www.fao.org/home/en/#')
FAO_GEOMS = Namespace()

namespaces = {
    'dct': DCT,
    'gsp': GSP,
    'gkq': GKQ,
    'profile': PROFILE,
    ':': EX,
    'fao': FAO,
    'skos': SKOS
}


g = Graph()
for prefix, namespace in namespaces.items():
    g.bind(prefix, namespace)

g.add((FAO.globalEcologicalZones, RDF.type, SKOS.Concept))
g.add((FAO.globalEcologicalZones, SKOS.prefLabel, Literal('Global Ecological Zones')))
g.add((FAO.globalEcologicalZones, SKOS.definition, Literal(gez_def)))

g.add((FAO.globalEcologicalZones2010, RDF.type, SKOS.Concept))
g.add((FAO.globalEcologicalZones2010, SKOS.prefLabel, Literal('Global Ecological Zones 2010')))
g.add((FAO.globalEcologicalZones2010, SKOS.definition, Literal(gez2010_def)))
g.add((FAO.globalEcologicalZones2010, SKOS.narrower, FAO.globalEcologicalZones))

g.add((FAO.globalEcologicalZones2010Tropical, RDF.type, SKOS.Concept))
g.add((FAO.globalEcologicalZones2010Tropical, SKOS.prefLabel, Literal('Tropical Ecological Zones 2010')))
g.add((FAO.globalEcologicalZones2010Tropical, SKOS.definition, Literal('All months without frost: in marine areas over 18°C')))
g.add((FAO.globalEcologicalZones2010Tropical, SKOS.narrower, FAO.globalEcologicalZones2010))
g.add((FAO.globalEcologicalZones2010Tropical, RDF.type, DCT.Location))
g.add((FAO.globalEcologicalZones2010Tropical, RDF.type, GSP.Feature))
tropical_geom = BNode()
g.add((FAO.globalEcologicalZones2010Tropical, GSP.hasDefaultGeometry, tropical_geom))
g.add((tropical_geom, GSP.asWKT, Literal(tropical_polygon.simplify(1).wkt)))

g.add((FAO.globalEcologicalZones2010Subtropical, RDF.type, SKOS.Concept))
g.add((FAO.globalEcologicalZones2010Subtropical, SKOS.prefLabel, Literal('Subtropical Ecological Zones 2010')))
g.add((FAO.globalEcologicalZones2010Subtropical, SKOS.definition, Literal('Eight months or more over 10°C')))
g.add((FAO.globalEcologicalZones2010Subtropical, SKOS.narrower, FAO.globalEcologicalZones2010))
g.add((FAO.globalEcologicalZones2010Subtropical, RDF.type, DCT.Location))
g.add((FAO.globalEcologicalZones2010Subtropical, RDF.type, GSP.Feature))
subtropical_geom = BNode()
g.add((FAO.globalEcologicalZones2010Subtropical, GSP.hasDefaultGeometry, subtropical_geom))
g.add((subtropical_geom, GSP.asWKT, Literal(subtropical_polygon.simplify(1).wkt)))

g.add((FAO.globalEcologicalZones2010Temperate, RDF.type, SKOS.Concept))
g.add((FAO.globalEcologicalZones2010Temperate, SKOS.prefLabel, Literal('Temperate Ecological Zones 2010')))
g.add((FAO.globalEcologicalZones2010Temperate, SKOS.definition, Literal('Four to eight months over 10°C')))
g.add((FAO.globalEcologicalZones2010Temperate, SKOS.narrower, FAO.globalEcologicalZones2010))
g.add((FAO.globalEcologicalZones2010Temperate, RDF.type, DCT.Location))
g.add((FAO.globalEcologicalZones2010Temperate, RDF.type, GSP.Feature))
temperate_geom = BNode()
g.add((FAO.globalEcologicalZones2010Temperate, GSP.hasDefaultGeometry, temperate_geom))
g.add((temperate_geom, GSP.asWKT, Literal(temperate_polygon.simplify(1).wkt)))

g.add((FAO.globalEcologicalZones2010Boreal, RDF.type, SKOS.Concept))
g.add((FAO.globalEcologicalZones2010Boreal, SKOS.prefLabel, Literal('Boreal Ecological Zones 2010')))
g.add((FAO.globalEcologicalZones2010Boreal, SKOS.definition, Literal('Up to 3 months over 10°C')))
g.add((FAO.globalEcologicalZones2010Boreal, SKOS.narrower, FAO.globalEcologicalZones2010))
g.add((FAO.globalEcologicalZones2010Boreal, RDF.type, DCT.Location))
g.add((FAO.globalEcologicalZones2010Boreal, RDF.type, GSP.Feature))
boreal_geom = BNode()
g.add((FAO.globalEcologicalZones2010Boreal, GSP.hasDefaultGeometry, boreal_geom))
g.add((boreal_geom, GSP.asWKT, Literal(boreal_polygon.simplify(1).wkt)))

g.add((FAO.globalEcologicalZones2010Polar, RDF.type, SKOS.Concept))
g.add((FAO.globalEcologicalZones2010Polar, SKOS.prefLabel, Literal('Polar Ecological Zones 2010')))
g.add((FAO.globalEcologicalZones2010Polar, SKOS.definition, Literal('All months below 10°C')))
g.add((FAO.globalEcologicalZones2010Polar, SKOS.narrower, FAO.globalEcologicalZones2010))
g.add((FAO.globalEcologicalZones2010TPolar, RDF.type, DCT.Location))
g.add((FAO.globalEcologicalZones2010TPolar, RDF.type, GSP.Feature))
polar_geom = BNode()
g.add((FAO.globalEcologicalZones2010TPolar, GSP.hasDefaultGeometry, polar_geom))
g.add((polar_geom, GSP.asWKT, Literal(polar_polygon.simplify(1).wkt)))

g.add((FAO.globalEcologicalZones2010Water, RDF.type, SKOS.Concept))
g.add((FAO.globalEcologicalZones2010Water, SKOS.prefLabel, Literal('Global Ecological Zones 2010 - Water')))
g.add((FAO.globalEcologicalZones2010Water, SKOS.narrower, FAO.globalEcologicalZones2010))
g.add((FAO.globalEcologicalZones2010Water, RDF.type, DCT.Location))
g.add((FAO.globalEcologicalZones2010Water, RDF.type, GSP.Feature))
water_geom = BNode()
g.add((FAO.globalEcologicalZones2010Water, GSP.hasDefaultGeometry, water_geom))
g.add((water_geom, GSP.asWKT, Literal(water_polygon.simplify(1).wkt)))

g.serialize('globalEcologicalZones.ttl', format='ttl')
