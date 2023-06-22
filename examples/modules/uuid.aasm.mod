!name UUID

!targets
spade


!instructions
GETUUID ModVar a
ISEQ ModVar a, ModVar b

!preamble spade
import uuid

!impl GETUUID spade
a = str(uuid.uuid4())


