%targets
spade

%instructions
GETUUID ModVar

%preamble spade
import uuid

%impl GETUUID spade
ModVar = str(uuid.uuid4())


