!name UUID

!targets
spade

!types
uuid

!instructions
GETUUID a: mut uuid
ISEQ a: uuid, b: uuid

!preamble spade
import uuid

!impl GETUUID spade
a = str(uuid.uuid4())


