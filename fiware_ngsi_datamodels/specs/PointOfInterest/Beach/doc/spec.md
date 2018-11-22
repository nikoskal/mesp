# Beach

## Description

<!-- textlint-disable no-dead-link -->
This entity contains a harmonised geographic description of a beach. It is used
in applications that use spatial data and is applicable to Tourism, Environment,
and Smart City vertical segments and related IoT applications. Special thanks to
[TURESPAÑA](https://www.tourspain.es/en-us) who provided some
examples which inspired the development of this data model.
<!-- textlint-enable no-dead-link -->

## Data Model

A JSON Schema corresponding to this data model can be found
[here](http://fiware.github.io/dataModels/specs/PointOfInterest/Beach/schema.json).
This entity type has been designed as an extension of
[https://schema.org/Beach](https://schema.org/Beach) so that any property
specified by schema.org and which domain is `https://schema.org/Beach` can be
used by applications.

-   `id` : Unique identifier.

-   `type` : Entity type. It must be equal to `Beach`.

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.
    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.
-   `source` : A sequence of characters giving the source of the entity data.
    -   Attribute type: [Text](https://schema.org/Text) or
        [URL](https://schema.org/URL)
    -   Optional
-   `name` : Name of this beach.
    -   Normative References: [https://schema.org/name](https://schema.org/name)
    -   Mandatory
-   `alternateName` : Alternative name for this beach.

    -   Normative References:
        [https://schema.org/alternateName](https://schema.org/alternateName)
    -   Optional

-   `description` : Description of this beach.

    -   Normative References:
        [https://schema.org/description](https://schema.org/description)
    -   Optional

-   `location` : Location of this beach represented by a GeoJSON geometry,
    usually a `Point` or a Polygon.
    -   Attribute type: `geo:json`.
    -   Normative References:
        [https://tools.ietf.org/html/rfc7946](https://tools.ietf.org/html/rfc7946)
    -   Mandatory if `address` is not defined.
-   `address` : Address of this beach.

    -   Normative References:
        [https://schema.org/address](https://schema.org/address)
    -   Mandatory if `location` is not present.

-   `width` : Width of this beach.

    -   Normative References:
        [https://schema.org/width](https://schema.org/width)
    -   Default unit: meter
    -   Optional

-   `length` : Length of this beach.
    -   Normative References:
        [https://schema.org/length](https://schema.org/lenght)
    -   Default unit: meter
    -   Optional
-   `beachType` : Type of beach according to different criteria.

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed Values: (`whiteSand`, `urban`, `isolated`, `calmWaters`,
        `blueFlag`, `Q-Quality`, `strongWaves`, `windy`, `blackSand`) or any
        other value needed by an application.
    -   Optional

-   `occupationRate` : Typical occupation rate of this beach.

    -   Attribute type: [Text](https://schema.org/Text)
    -   Allowed Values: (`low`, `medium`, `high`)
    -   Optional

-   `facilities` : Describes different facilities offered by this beach.

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values: (`promenade`, `showers`, `cleaningServices`,
        `lifeGuard`, `sunshadeRental`, `sunLoungerRental`, `waterCraftRental`,
        `toilets`, `touristOffice`, `litterBins`, `telephone`,
        `surfPracticeArea`, `accessforDisabled`) or any other value needed by an
        application.
    -   Optional

-   `accessType` : Describes how to get to this beach.

    -   Attribute type: List of [Text](https://schema.org/Text)
    -   Allowed values: (`privateVehicle`, `boat`, `onFoot`, `publicTransport`)
    -   Optional

-   `refSeeAlso` : Reference to one or more related entities.
    -   Attribute type: List of References
    -   Optional

## Examples of use

    {
         "id": " Beach-A-Concha-123456 ",
         "type": ”Beach",
         "name": "Playa de a Concha",
         "description": "La Playa de A Concha se presenta .....",
         "address": {
            "addressCountry": "ES",
            "addressLocality": "Vilagarcía de Arousa"
         },
         "beachType": ["whiteSand", "urban", "calmWaters"],
         "occupationRate": "high",
         "facilities": ["promenade", "showers", "cleaningServices", "lifeGuard"],
         “accessType”: ["privateVehicle", "onFoot", "publicTransport"],
         "location": {
            "type": "Point",
            "coordinates": [-8.768460000000001, 42.60214472222222]
         },
         “width”: 51,
         “length”: 450,
         "source": "http://www.tourspain.es"
    }

## Use it with a real service

Coming soon

## Open Issues
