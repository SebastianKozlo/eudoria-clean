# P07_SERIALIZE_HEAD HANDOFF
Verdict: The containing function is a large serializer: CALL EDI repeatedly converts a float local to double (FSTP qword [ESP]) and writes it, TEST EAX,0x207 error-checking each write (file-writer semantic, cl
Frontier: see REPORT/CLAIMS and root FIRST_MISSING_EDGE.
