!name UUID

!description
Simple module to use uuids.
Provides a single function, GETUUID, which returns a uuid as a string.

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


