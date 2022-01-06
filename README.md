mactool
=======
A simple MAC address database and generator.

Features
--------
- Random MAC generator
- Local database of OUI vendors
- Vendor bytes query (get vendor string from vendor bytes)
- Vendor string query (get vendor bytes from vendor string)

Examples
--------
+ Generate a MAC address belonging to Amazon Technologies Inc.
```
$ mactool -gv Amazon
C8:6C:3D:58:25:0F
```

+ Search the vendor of a MAC address
```
$ mactool -b 00:21:02
LEXMARK INTERNATIONAL, INC.
```
