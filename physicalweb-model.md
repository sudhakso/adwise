@startuml

Venue "1" *-- "many" Sensor : aggregation
Sensor <|-- MediaSource
OOHMediaSource <|-- MediaSource
DigitalMediaSource <|-- MediaSource
MediaAggregate "1" *-- "many" Venue: aggregation
OOHMediaSource "1" *-- "1" Venue: aggregation
MediaAggregate "1" *-- "many" AmenityExtension: contains
AmenityExtension "1" *-- "many" Venue: aggregation
MediaSource --> "plays" Campaign
MediaAggregate "1" *-- "many" DigitalMediaSource


@enduml
