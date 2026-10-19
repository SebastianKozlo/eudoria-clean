# FLOW - value graph extension (pair -> pump -> returned EAX)

E-PAIR0: pair[0] @00823C41 -> stored to ARG1 slot -> passed BY ADDRESS to 004D1430(this=receiver+4) @00823C57 -> also drives sub-object selection (local==EDI+4 -> EDI+=0x1C else EDI=local+0x14). Status: CONFIRMED.
E-PAIR1: pair[1] @00823D16 -> arg1 of loop resolver virtual [[entry+8]vtable+0x4] @00823D24. Status: CONFIRMED (loop path).
E-RET-FAST: EAX = [[EDI+0x24]vtable+0x38](pair_ptr) @00823C84 -> ESI -> [if !=0] TLS flag reset -> vtable+8 -> 00826760(this=ESI,arg2,arg3) -> EAX=ESI @00823E42. Status: CONFIRMED.
E-RET-LOOP: EAX = [[entry+8]vtable+0x4](pair[1],&local) @00823D24 -> ESI -> 00826840(this=ESI,pair_ptr) -> [[EDI+0x24]vtable+0x3C](&[ESP+0x24],ESI) -> optional [[saved_this+0x58]vtable+0x4](ESI) -> TLS flag set -> finish via 00823E27 -> 00826760(this=ESI,arg2,arg3) -> EAX=ESI. Status: CONFIRMED.
E-NULL: returns 0 from 00823CAE / 00823DFF. Status: CONFIRMED.
GLOBAL-ELEMENT-ORIGIN: adapter 006C29D0 returns pump EAX (P01); closed prior P06/P07 copy this DWORD into global vector 0x00BA45E8 element (tail+=4). Therefore global element kind = resolver-produced OBJECT POINTER (or 0). This upgrades P02's GLOBAL_ELEMENT_KIND:NOT_ESTABLISHED to OBJECT_POINTER_OR_ZERO (by this-use evidence @00823D31/00823E3B), while DATA_DOMAIN of the objects remains NOT_ESTABLISHED.
