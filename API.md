# API and CLI interfaces #

CLI commands that can be used to interact with the system

### APIs that do operation on 'mediaaggregate' ###
adwise list mediaaggregate

adwise create mediaaggregate 

adwise addimage mediaaggregate --id <mediaaggregate-id> --icon <file path> --home <file path>

adwise add mediaaggregate --id <mediaaggregate-id> -type <campaign|amenity> --id <campaign-id|amenity-id>

### APIs that do operation on 'campaign' ###
adwise list campaign

adwise list campaign --mediaaggregate-id=<aggregate-id>

adwise create campaign

adwise addimage campaign --id <campaign-id> --file <file path>


### APIs that do operation on 'amenity' ###
adwise list amenity

adwise list amenity --mediaaggregate-id=<aggregate-id>

adwise create amenity

adwise addimage amenity --id <amenity-id> --file <file path>

### APIs that do operation on 'imagead' ###
adwise list imagead

adwise create imagead --campaign-id <campaign-id>

adwise addimage imagead --id <ad-id> --file <file path>


