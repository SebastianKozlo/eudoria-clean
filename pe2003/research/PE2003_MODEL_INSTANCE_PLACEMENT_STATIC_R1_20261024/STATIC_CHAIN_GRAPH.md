# STATIC_CHAIN_GRAPH — PE2003_MODEL_INSTANCE_PLACEMENT_STATIC_R1_20261024

Both models share this chain (differences noted). [X] = byte-proven CONFIRMED; [~] = bounded negative / boundary; [?] = runtime-only operand (static unreachable).

UDP server stream -> [X] reliable-UDP pump (recvfrom @0x5BF918, flags 0x10/0x08)
 -> [X] message deserializer (FUN_005bb321 writes +0x2C; records 0x1C {id, wire-u32, TLV tag0/tag3 f32...})
 -> [X] definition registry loader FUN_005977b0 -> RB-tree @GCE+0x10064
 -> [X] executor FUN_00454300 (immediate | [X] deferred queue +0x1001C drained by state-machine tick)
 -> [X] VM interpreter FUN_00454360 executes DLOB bytecode of def 4508/4057
      -> [X] property getters return resource ids in VM register C (consumed host-side)
      -> [X] engine lookups 4652 (ENVIRONMENT strings) / 4653 (PDAT resource table) via dispatcher 0x441DF0
      -> [X] CALL_abs[0] binder-patched external bytecode [? patch values = runtime]
      -> [X] per-part loop: 26 parts (4508) / 18 parts (4057) -> ATTACH ext 30298 (def 1796, forwarder)
      -> [~] ext 33521 class 2202 — bytecode NOT in local corpus (1936-member census negative)
 -> [X] native model instance get-or-create FUN_0051f6e0 (cache map; miss -> clone root from NIF template)
      -> [X] clone STRUCTURAL (values default; template NIF roots are identity)
 -> [X] SceneInstancePair 0x10 {id, holder} via ScriptInsert case 15497 (batch, id-only) / other 4 callsites
 -> [X] add to scene = slot-append, identity only, no transform at add
 -> [X] transform writers (final set): default reset / default-init ctors / GCE 0x10a+0xdc (sub-model, VM constants) / FUN_005030c0 (root, record[6] entities only)
      -> [X] FUN_005030c0 source = message struct 0x48 (translation world/100 + euler radians + internal state)
 -> [X] placement commands 0x14/0x18 forward node values to queue targets [? target identity runtime]
 -> [~] OUR MODELS: no local value source anywhere (corpus 1936, EXTN path 7134 dwords, TDF 51921, install 704 files, 2234 recipes — all negatives with recorded scopes)
 => PE2003_HISTORICAL_PLACEMENT = NOT_ESTABLISHED from local static data; WORLD_XYZ_RECOVERED = NO.
