!name LISTS

!description
targets: spade
Instructions:
GETUUID will generate a new uuid and store it in the declared variable.
ISEQ will compare two uuids and return true if they are equal.
ISNEQ will compare two uuids and return true if they are not equal.

!targets
spade

!types

!instructions
SUM a: mut list_float, dst: float

!preamble spade

!impl SUM spade
return sum(a)
