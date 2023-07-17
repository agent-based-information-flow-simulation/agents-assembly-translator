!name UUID

!description
Simple module to use uuids.
Provides functionality to utilise uuids.
targets: spade
Introduces one type: uuid.
Instructions:
GETUUID will generate a new uuid and store it in the declared variable.
ISEQ will compare two uuids and return true if they are equal.
ISNEQ will compare two uuids and return true if they are not equal.

!targets
spade

!types
uuid

!instructions
GETUUID a: mut uuid
ISEQ* a: uuid, b: uuid
ISNEQ* a: uuid, b: uuid

!preamble spade
import uuid

!impl GETUUID spade
a = str(uuid.uuid4())

!impl ISEQ spade
if a == b:
  return True
return False

!impl ISNEQ spade
if a != b:
  return True
return False
