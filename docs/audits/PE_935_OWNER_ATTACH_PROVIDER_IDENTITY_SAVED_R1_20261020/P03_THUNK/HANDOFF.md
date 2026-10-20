# P03_THUNK HANDOFF
Verdict: 0085BF00 is a cdecl 2-arg adapter DeserializeThunk(ARG1=reader,[ESP+4]; ARG2=OBJ,[ESP+8]): ECX:=ARG2 becomes this for 0085BD80, ARG1 pushed as its reader arg, returns ARG1 in EAX. 0085BF20 init-writes
Frontier: see REPORT/CLAIMS and root FIRST_MISSING_EDGE.
