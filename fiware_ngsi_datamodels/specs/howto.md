# How to use FIWARE Harmonised Data Models in your projects

This section aims to provide few simple guidelines for the adoption of FIWARE
Harmonised Data Models. Readers interested into modifying or creating new data
models should refer to [Data models guidelines](guidelines.md). This guide is
not exhaustive and does not aim to cover the specifics of each model, rather it
provides general usage tips valid for most of the existing models and for
expected models in the future.

Data Models have been defined in relation to the FIWARE reference data context
model ([NGSI v2](http://fiware.github.io/specifications/ngsiv2/stable/)). While
this does not imply that they cannot be used outside of the NGSI context model,
it does however indicate that some of [design principles](guidelines.md) have
been driven by that. This also implicitly means that Data Models will follow the
evolution of FIWARE platform,
[NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/004/01.01.01_60/gs_CIM004v010101p.pdf)
mappings will be added to all existing Data Models in the medium term.

## General principles

The general principle guiding your adoption should be: keep it simple.

-   **Use only the parts of the Data Model your application really need.** This
    will help reducing the amount of information exchanged to the one you need
    and not more than that. This may apply also just to a part of your
    application. I.e. while you use in your Context Broker the whole Data Model,
    to other services you may dispatch only the needed part.
-   **Use metadata only in case of need, and follow the assumptions provided in
    the Data Model.** For example, in case your application is leveraging the
    default unit defined in a Data Model (e.g. meters), avoid attaching metadata
    to annotate the unit. In case your application is using a different unit, do
    annotate it, it will simplify data exchange with other systems in case of
    need.
-   **Stick to the existing Data Models.** Data Models are meant to be an effort
    to facilitate interoperability within the community. If you change the
    meaning or the data type attached to an attribute, this will break
    interoperability. Of course it may be the case that the model is not
    covering your scenario, or it contains errors. Open a ticket in the
    repository, and let the community discuss on the issue!
    [Contribute](guidelines.md) to the evolution of the model! In doing so
    please keep in mind the
    [guidelines to create new data models](guidelines.md).
-   **While not generally advised, you can add additional attributes in your
    specific application for the purpose of your application.** Be aware that of
    course this means that such attributes may not be correctly used by other
    applications leveraging the same Data Model. We recommend, if the attribute
    you want to add is of general adoption and not specific to your case, to
    propose it to become officially part of the Data Model. You can open an
    issue or a pull request for that.
-   **Data Models, in most of the cases, are NGSI v2 codification of existing
    data models.** You can find the references in each Data Model specification,
    but for the sake of maintainability, on purpose we don't report the full
    specification. This means that to gather further details, you need to access
    the original source. For example, for the location, we use GeoJSON. You can
    find the exact semantics of GeoJSON schema in the related standard.
-   Be aware that **[JSON Schemas](http://json-schema.org/) provided cover only
    the so called _key-value_ representation of NGSI v2 context data**.
-   Be aware that at the time being **none of the official FIWARE Core Enablers
    enforce schema validation**. Thus, in case you want to be sure your
    application data validates correctly against a given Data Model, this is up
    to you.

## Going through a Data Model

Each Data Model is programmatically defined using a
[JSON Schema](http://json-schema.org/), as previously mentioned, the JSON schema
covers only the so called _key-value_ representation of NGSI v2 context data.
Thus the JSON Schema does not cover the _normalised_ representation of context
data.

In the [NGSI v2](http://fiware.github.io/specifications/ngsiv2/stable/)
normalised format each attribute (`key`) of the Data Model is represented by a
JSON object with the following syntax:

-   The attribute value is specified by the `value` property, whose value may be
    any JSON datatype.
-   The attribute NGSI type is specified by the `type` property, whose value is
    a string containing the NGSI type.
-   The attribute metadata is specified by the `metadata` property. Its value is
    another JSON object which contains a property per metadata element defined
    (the name of the property is the `name` of the metadata element). Each
    metadata element, in turn, is represented by a JSON object containing the
    following properties:
    -   `value`: Its value contains the metadata value, which may correspond to
        any JSON datatype.
    -   `type`: Its value contains a string representation of the metadata NGSI
        type.

```json
{
    "id": "entityId",
    "type": "entityType",
    "att1": {
        "value": "value1",
        "type": "Text",
        "metadata": {
            "metada1": {
                "value": "metavalue1"
            }
        }
    }
}
```

In the case of the key-value format (also known as _Simplified Entity
Representation_ in the
[NGSI v2](http://fiware.github.io/specifications/ngsiv2/stable/) specification),
values are directly mapped to the keys, and metadata are not covered:

```json
{
    "id": "entityId",
    "type": "entityType",
    "att1": "value1"
}
```

Of course the normalised format contains richer information, but on the other
side it is redundant and less efficient in term of transport.

To clarify the difference among the two representation here is a complete
example from the `AirQualityObserved` Data Model:

-   Normalised format:

```json
{
    "id": "Madrid-AmbientObserved-28079004-2016-03-15T11:00:00",
    "type": "AirQualityObserved",
    "dateObserved": {
        "value": "2016-03-15T11:00:00/2016-03-15T12:00:00"
    },
    "airQualityLevel": {
        "value": "moderate"
    },
    "CO": {
        "value": 500,
        "metadata": {
            "unitCode": {
                "value": "GP"
            }
        }
    },
    "temperature": {
        "value": 12.2
    },
    "NO": {
        "value": 45,
        "metadata": {
            "unitCode": {
                "value": "GQ"
            }
        }
    },
    "refPointOfInterest": {
        "type": "Relationship",
        "value": "28079004-Pza.deEspanya"
    },
    "windDirection": {
        "value": 186
    },
    "source": {
        "value": "http://datos.madrid.es"
    },
    "windSpeed": {
        "value": 0.64
    },
    "SO2": {
        "value": 11,
        "metadata": {
            "unitCode": {
                "value": "GQ"
            }
        }
    },
    "NOx": {
        "value": 139,
        "metadata": {
            "unitCode": {
                "value": "GQ"
            }
        }
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-3.712247222222222, 40.423852777777775]
        }
    },
    "airQualityIndex": {
        "value": 65
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressCountry": "ES",
            "addressLocality": "Madrid",
            "streetAddress": "Plaza de Espa\u00f1a"
        }
    },
    "reliability": {
        "value": 0.7
    },
    "relativeHumidity": {
        "value": 0.54
    },
    "precipitation": {
        "value": 0
    },
    "NO2": {
        "value": 69,
        "metadata": {
            "unitCode": {
                "value": "GQ"
            }
        }
    },
    "CO_Level": {
        "value": "moderate"
    }
}
```

-   key-value format:

```json
{
    "id": "Madrid-AmbientObserved-28079004-2016-03-15T11:00:00",
    "type": "AirQualityObserved",
    "address": {
        "addressCountry": "ES",
        "addressLocality": "Madrid",
        "streetAddress": "Plaza de España"
    },
    "dateObserved": "2016-03-15T11:00:00/2016-03-15T12:00:00",
    "location": {
        "type": "Point",
        "coordinates": [-3.712247222222222, 40.423852777777775]
    },
    "source": "http://datos.madrid.es",
    "precipitation": 0,
    "relativeHumidity": 0.54,
    "temperature": 12.2,
    "windDirection": 186,
    "windSpeed": 0.64,
    "airQualityLevel": "moderate",
    "reliability": 0.9,
    "CO": 500,
    "NO": 45,
    "NO2": 69,
    "NOx": 139,
    "SO2": 11,
    "CO_Level": "good",
    "NO_Level": "moderate",
    "refPointOfInterest": "28079004-Pza. de España"
}
```

For each Data Model we provide a set of examples (in some cases also using the
Normalised representation of NGSI v2), such examples have been validated against
the respective JSON Schema and against a
[Orion Context Broker](https://fiware-orion.readthedocs.io/en/master/) instance
(to ensure that also the content encoding is compliant with the reference
implementation).

As a consequence of the NGSI v2 specifications, all Data Models must include the
following attributes:

-   `id` : a unique identified of the entity modelled.
-   `type` : The entity type, i.e. the type of Data Model, e.g. `Alert`.
-   `dateModified` : Last update timestamp of the entity.
-   `dateCreated` : The entity's creation timestamp.

`dateCreated` and `dateModified` are special entity attributes provided
off-the-shelf by NGSI v2 implementations.

Most of the FIWARE Data Models adopt the
[GSMA common definitions](https://fiware.github.io/dataModels/common-schema.json),
and so also include standard GSMA terminology such as:

-   `owner`: An array of URIs or pointers to NGSI entities representing the
    owner(s) of the entity.
-   `source`: A pointer (eventually an URI) to the service providing the data.
-   `name`: A mnemonic name given to the entity.
-   `alternateName`: An alternative mnemonic name given to the entity.
-   `description`: A textual description of the entity.
-   `dataProvider`: A name identifying the entity providing the data.

See for example the [`Building` Data Model](Building/Building/doc/spec.md).

Similarly most of the FIWARE Data Models adopt the
[Location common definitions](https://fiware.github.io/dataModels/common-schema.json),
and thus include the following attributes:

-   `address`: the civic address of the entity as per
    [schema.org](http://schema.org/address).
-   `location`: the [GeoJSON](https://tools.ietf.org/html/rfc7946)
    representation of the entity location.

See for example the [`Building` Data Model](Building/Building/doc/spec.md).

GeoJSON supports the definition of quite complex geometries (`Point`,
`LineString`, `Polygon`, `MultiPoint`, `MultiLineString`, and `MultiPolygon`)
representing the localisation of entities. Examples of GeoJSON geometries are
available [here](https://tools.ietf.org/html/rfc7946#appendix-A).

## General tips

### How to specify units of measurement

1. If your data use the default unit defined in the Data Model, you don't need
   to specify any. It is implied.
1. Unless explicitly stated otherwise, all FIWARE data models use the metric
   system of measurements by default. Regardless the model specification include
   explicit reference to the scale adopted.
1. If your data use a different unit, you will need to use the `unitCode`
   metadata annotation in your data (and you will need to adopt the normalised
   representation). Code used should be the ones defined by
   [UN/CEFACT](https://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20_rev3_Annex3e.pdf).
   E.g.:

```json
"length": {
    "value": 11,
    "metadata": {
        "unitCode": {
            "value": "FOT"
        }
    }
}
```

### How to attach specific time of update to a single attribute

Often, different attributes of the same entity are updated at different points
in time as the result of data aggregation across measurements from different
sensors. Note that the `dateModified` value only reflects only the point in time
the NGSI v2 implementation received an entity update, it does not correspond to
the moment in time at which an attribute changed. In order to be able to define
when a specific attribute changed you should you should use the `timestamp`
metadata annotation. E.g.:

```json
"speed": {
    "value": 11,
    "metadata": {
        "timestamp": {
            "value": "2016-03-15T11:00:00.000"
        }
    }
}
```

### Proper usage of relations among Data Models

With the introduction of
[NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/004/01.01.01_60/gs_CIM004v010101p.pdf),
a growing number attributes are being defined which represent relationships
between entities.

Previously the FIWARE data model defined the name of such attributes was normed
to be `ref` followed by the name of the Entity Type referenced by the attribute,
for example in the case of Entity Type `Device`, the full attribute would be
`refDevice`.

With the introduction of NGSI-LD, following the link with practises in the
ontologies, such attributes are defined with the usage of a verb (plus
optionally an object) such as `hasStop`, `operatedBy`, `hasTrip`, etc.

While in the first case, the entity type to be looked for is implicitly defined
by the attribute name, this is no longer the case with NGSI-LD, that's why it is
important to use NGSI-LD [URNs](https://tools.ietf.org/html/rfc8141) that convey
the type of the target entity, for instance `urn:ngsi-ld:gtfs:Stop:S123`.

Currently it is up to the logic of your application to include the logic to
navigate entity relationships, as it is not yet defined within implementations
of the NGSI v2 or NGSI-LD specification.

## TODO

-   Add paragraph _Validate your own examples_
