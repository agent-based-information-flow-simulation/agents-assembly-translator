%name UUID

%targets
spade

%instructions
GETUUID ModVar

%preamble spade
import uuid

%impl GETUUID spade
$1 = str(uuid.uuid4())
