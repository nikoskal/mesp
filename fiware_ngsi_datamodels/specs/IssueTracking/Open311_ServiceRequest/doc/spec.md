# Open 311 Service Request

An entity of type `ServiceRequest` is an acceptable Open 311 service request.
Such entity encompasses all the properties defined by Open 311 at
[POST Service Request](http://wiki.open311.org/GeoReport_v2/#post-service-request)
and
[GET Service Request](http://wiki.open311.org/GeoReport_v2/#get-service-request).

Using this data model and a FIWARE NGSI version 2 implementation it is
straightforward to implement a service compliant with the Open 311
specifications.

## Data Model

The data model is defined as shown below:

-   `id` : Entity's unique identifier. It might be equal to a string
    representation of `service_request_id`.

-   `type` : It must be `Open311:ServiceRequest`.

The following fields defined by Open 311 are allowed to be attributes of this
entity type:

-   `service_request_id`

-   `jurisdiction_id`

-   `service_code`

-   `service_name`

-   `description`

-   `agency_responsible`. Please note that this is semantically equivalent to
    the [provider](http://schema.org/provider) property (name subproperty) of
    schema.org.

-   `service_notice`

-   `address_string`

-   `address_id`

-   `zipcode`

-   `status`

-   `status_notes`

-   `requested_datetime`

-   `updated_datetime`

-   `expected_datetime`

-   `lat`

-   `long`

-   `media_url`

-   `email`

-   `first_name`

-   `last_name`

-   `phone`

-   `device_id`

-   `account_id`

-   `address`. If used it must be renamed to `open311:address`.

_All attribute types must be coherent with the Open 311 definitions.
Applications must use the types `Text`, `Number` and `DateTime` accordingly._

To support FIWARE NGSI v2 geoqueries concerning Open311 Service Requests the
following property must be added:

-   `location` : Location of the area on which this service request is
    concerned.
    -   Attribute type: GeoJSON geometry.
    -   Mandatory if the service request is geolocated.

Additionally, applications might use the following standard schema.org
structured properties:

-   [address](http://schema.org/address).
-   [contactPoint](http://schema.org/contactPoint)

_Note 1: Applications are responsible of keeping consistency between the
`location` field and the Open 311 `lat` and `long` fields_. _The same can be
said about_:

-   `address` property and the Open 311 fields related to it (`zipcode`,
    `address_string`, etc.).
-   `contactPoint` property and fields like (first_name, last_name, etc.)\*

_Note 2: This NGSI data model does not allow the use of `address` property
defined by Open 311. This has been done on purpose as we want to keep the
`address` property consistent with
[http://schema.org/address](http://schema.org/address). Applications are
encouraged to use `address_string` instead and do the corresponding mapping at
the adaptation layer._

To support the `attribute` parameter of Open 311 service requests this NGSI data
model adds the following property (please note it has been pluralized, to keep
consistency with `ServiceType`):

-   `attributes` : It is a dictionary with a key per attribute defined by the
    corresponding `ServiceType`. The key-value is always an array of strings. If
    an attribute is singled valued then such array will only contain one
    element. + Attribute type:
    [StructuredValue](https://schema.org/StructuredValue). + Optional

**Note**: JSON Schemas only capture the NGSI simplified representation, this
means that to test the JSON schema examples with a
[FIWARE NGSI version 2](http://fiware.github.io/specifications/ngsiv2/stable)
API implementation, you need to use the `keyValues` mode (`options=keyValues`).

## Examples of use

    {
      "id": "service-request:638344",
      "type": "Open311:ServiceRequest",
      "service_request_id": 638344,
      "status": "closed",
      "status_notes": "Duplicate request.",
      "service_name": "Aceras",
      "service_code": 234,
      "description": "Acera en mal estado con bordillo partido en dos",
      "agency_responsible": "Ayuntamiento de Ciudad",
      "requested_datetime": "2010-04-14T06:37:38-08:00",
      "updated_datetime": "2010-04-14T06:37:38-08:00",
      "expected_datetime": "2010-04-15T06:37:38-08:00",
      "address_string": "Calle San Juan Bautista, 2",
      "attributes": {
         "ISSUE_TYPE": ["Bordillo"]
      },
      "location": {
        "type": "Point",
        "coordinates": [  -3.164485591715449, 40.62785133667262 ]
      },
      "media_url":"http://exaple.org/media/638344.jpg"
    }

## Test it with real services

## Open issues
