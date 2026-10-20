# OWNER_ATTACH_TRACE (merged with PROVIDER_IDENTITY / RETURN_STORAGE per contract small-table merge)

B (owner, ECX in caller 00527AB0) -[load M32[B+0xC] @00527AB7? standing prior]-> R (receiver of CALL 0085BFA0 @00527AF9).
This run tested WHERE B attaches R:
- store+C@0085ACE9 (P01): REJECTED - stack local zero-init of out-buffer pair for CALL 00730F00; receiver ECX=ARG1; no B field write.
- next owner-attach edge: still unknown; the two commissioned candidates are exhausted negative; see FIRST_MISSING_EDGE frontier.

PROVIDER_IDENTITY_TRACE:
- store+2C@0085BE70 (P02-P04): REJECTED as P writer - global float-constant trio into stack-temp OBJ (+0x28/+0x2C/+0x30); OBJ constructed by 0085BBE0 at [ESP+0x18] of 0048EDxx loader via cdecl adapter 0085BF00 (sole caller 0048EDF7).
- store+2C@0085C0A7 (P05): REJECTED - float slot of 13-dword transform write to [EAX]=[ESP+0xAC].
- store+2C@0085CD17 (P06-P08): NEW STRONG CANDIDATE - product of virtual factory call (receiver [ESI+0x28], vtable slot+0x18) stored into [ESI+0x2C]; ESI=[ESP+0x34]; provider object exhibits vtable slots +0xAC (float getter), +0xB0 (3-float out), +0x4C/+0x50. Join ESI==R NOT established (entry binding missing). If joined: R+0x28=factory owner, R+0x2C=P writer site, P methods include slot+0xAC/+0xB0/+0x4C/+0x50; the 0085BFA0 read P->VT->VT+0x24->F->T then has a concrete P producer.

RETURN_STORAGE_TRACE:
- T=retval CALL F @0085BFB5 (standing prior); origin of T contents NOT advanced this run (Etap C not reached; slot+0x24 target body unopened). RETURN_T_ORIGIN=UNKNOWN.

INSTANCE_RESOURCE_JOIN:
- No resource/model-id to scene-root edge established this run. MODEL_RESOURCE_INSTANCE_EDGE=NOT_ESTABLISHED.
