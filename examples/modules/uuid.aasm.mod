!name UUID

!targets
spade

!types
uuid

!instructions
GETUUID uuid a

!blocks
ISEQ uuid a, uuid b

!preamble spade
import uuid

!impl GETUUID spade
a = str(uuid.uuid4())


