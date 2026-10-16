# -*- coding: utf-8 -*-
"""PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016 — core: pins, reader, scanner, manifest."""
import sys, os, json, hashlib, struct, datetime

RUN_ID = "PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016"
CONTRACT_ERA = "PCG_9_3_5"
OUTPUT_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_WRAPPER_POINTER_NEIGHBORHOOD_R2_20261016"
EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE_PIN = 8015872
EXE_SHA256_PIN = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
REPO_PATH = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
EXPECTED_BASE_SHA_PREFIX = "6ba8f7d"

S7_PATH = os.path.join(REPO_PATH, r"docs\audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913\01_RAW\S7_VTABLE_STORE_SCAN.json")
Z3_PATH = os.path.join(REPO_PATH, r"docs\audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913\02_ANALYSIS\Z3_portals.md")
ZS9_PATH = os.path.join(REPO_PATH, r"docs\audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913\01_RAW\ghidra_output\ZS9_DISASM_FUN_00852750_full.txt")
WRAP_REPORT_PATH = os.path.join(REPO_PATH, r"docs\audits\PE_935_PARAMETER_CURSOR_UPSTREAM_WRAPPER_R1_20261016\REPORT.md")
WRAP_EVIDENCE_PATH = os.path.join(REPO_PATH, r"docs\audits\PE_935_PARAMETER_CURSOR_UPSTREAM_WRAPPER_R1_20261016\EVIDENCE.json")
WRAP_ROSTER_PATH = os.path.join(REPO_PATH, r"docs\audits\PE_935_PARAMETER_CURSOR_UPSTREAM_WRAPPER_R1_20261016\decode\INSTRUCTION_ROSTER.json")
GA3_PATH = os.path.join(REPO_PATH, r"docs\audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913\01_RAW\ghidra_output\GA3_VTABLE_ENTRIES.json")
CALLER_PKG_ORIG = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PARAMETER_CURSOR_CALLER_DISCOVERY_R1_20261016"
CALLER_PKG_REPO = os.path.join(REPO_PATH, r"docs\audits\PE_935_PARAMETER_CURSOR_CALLER_DISCOVERY_R1_20261016")
CALLER_MANIFEST_SHA_PIN = "96F20F6CA32D5977C8AAE8FF19C8A055C2CE8F3191A59C08DFEEEC5047015ABF"
CALLER_MANIFEST_SIZE_PIN = 2386
CALLER_MANIFEST_ROWS_PIN = 24
CALLER_PKG_PHYSICAL_PIN = 25

WIN_VA_START = 0x00A91CC0
WIN_VA_END = 0x00A91D40
WIN_SIZE = 128
SITE_SLOT15_VA = 0x00A91CFC
SITE_SLOT15_VALUE_PIN = 0x00852A30
N_SLOTS = 32
TARGETS = [WIN_VA_START + 4 * i for i in range(N_SLOTS)]

S7_CONTROLS = [
    {"control_id": "S7-C1", "class": "ArkPortalCell", "vtable_va": 0x00A91CF8, "slot_index": 14,
     "window_va": 0x00851EB7, "window_file_offset": 4529847,
     "window_hex": "8946048d4610c706f81ca90033db895e08895e0c",
     "expected_pattern_offset": 8, "expected_dword_start": 0x00851EBF},
    {"control_id": "S7-C2", "class": "ArkPortalCell", "vtable_va": 0x00A91CF8, "slot_index": 14,
     "window_va": 0x0085213D, "window_file_offset": 4530493,
     "window_hex": "8bd9895c2414c703f81ca9008b732885f6c74424",
     "expected_pattern_offset": 8, "expected_dword_start": 0x00852145},
    {"control_id": "S7-C3", "class": "ArkPortalResourceItem", "vtable_va": 0x00A91D04, "slot_index": 17,
     "window_va": 0x00852ACB, "window_file_offset": 4532939,
     "window_hex": "241c00000000c706041da900e8f0a8100083c404",
     "expected_pattern_offset": 8, "expected_dword_start": 0x00852AD3},
    {"control_id": "S7-C4", "class": "ArkPortalResourceItem", "vtable_va": 0x00A91D04, "slot_index": 17,
     "window_va": 0x00852B3A, "window_file_offset": 4533050,
     "window_hex": "8bf189742408c706041da9008b4e1085c9c74424",
     "expected_pattern_offset": 8, "expected_dword_start": 0x00852B42},
]

PRIOR_BASELINE_SLOTS = {
    0: ("0x0084D750", "GA3 ArkPortalCellGraph entry[3]"),
    1: ("0x0084C2C0", "GA3 ArkPortalCellGraph entry[4]"),
    2: ("0x00000001", "GA3 ArkPortalCellGraph entry[5]"),
    3: ("0x00AB3008", "GA3 ArkPortalCellGraph entry[6] (COL-class pointer, .rdata)"),
    4: ("0x008506B0", "GA3 ArkPortalCellGraph entry[7]"),
    5: ("0x0095D4FA", "GA3 ArkPortalCellGraph entry[8] (_purecall per GA3)"),
    6: ("0x0095D4FA", "GA3 ArkPortalCellGraph entry[9] (_purecall per GA3)"),
    7: ("0x00AB3050", "GA3/S4 COL of ArkPortalIdGenerator"),
    8: ("0x008506B0", "GA3 ArkPortalIdGenerator entry[0] (vtable head @0x00A91CE0)"),
    9: ("0x008506D0", "GA3 ArkPortalIdGenerator entry[1]"),
    10: ("0x008506D0", "GA3 ArkPortalIdGenerator entry[2]"),
    11: ("0x00000001", "GA3 ArkPortalIdGenerator entry[3]"),
    12: ("0x41800000", "GA3 ArkPortalIdGenerator entry[4]"),
    13: ("0x00AB309C", "GA3/S4 COL of ArkPortalCell"),
    14: ("0x00850C50", "GA3/VA_EVIDENCE_REGISTRY ArkPortalCell entry[0] (vtable head @0x00A91CF8)"),
    15: ("0x00852A30", "GA3/VA_EVIDENCE_REGISTRY/Z3 ArkPortalCell entry[1] = parameter-cursor wrapper (R1 audits)"),
    16: ("0x00AB30E4", "GA3/S4 COL of ArkPortalResourceItem"),
    17: ("0x00852B80", "S14 byte window @0x00A91D04 + GA3 ArkPortalResourceItem entry[0]"),
    18: ("0x008E0110", "S14 byte window + GA3 ArkPortalResourceItem entry[1]"),
    19: ("0x00826770", "S14 byte window + GA3 ArkPortalResourceItem entry[2]"),
    20: ("0x00000001", "S14 byte window + GA3 ArkPortalResourceItem entry[3]"),
    21: ("0x00AB3130", "GA3/S4 COL of ArkPortalPortal"),
    22: ("0x00852C90", "GA3 ArkPortalPortal entry[0] (vtable head @0x00A91D18)"),
    23: ("0x00852D60", "GA3 ArkPortalPortal entry[1]"),
    24: ("0x00000001", "GA3 ArkPortalPortal entry[2]"),
    25: ("0x3D23D70A", "GA3 ArkPortalPortal entry[3]"),
    26: ("0x471C4000", "GA3 ArkPortalPortal entry[4]"),
}
PRIOR_RAW_POSITIONS = {
    "0x00851EBF": {"slot_index": 14, "slot_va": "0x00A91CF8", "source": "S7 ArkPortalCell window 0x00851EB7 pattern@+8"},
    "0x00852145": {"slot_index": 14, "slot_va": "0x00A91CF8", "source": "S7 ArkPortalCell window 0x0085213D pattern@+8"},
    "0x00852AD3": {"slot_index": 17, "slot_va": "0x00A91D04", "source": "S7 ArkPortalResourceItem window 0x00852ACB pattern@+8"},
    "0x00852B42": {"slot_index": 17, "slot_va": "0x00A91D04", "source": "S7 ArkPortalResourceItem window 0x00852B3A pattern@+8"},
}
PRIOR_GA3_XREFS = {
    "8":  [{"from_va": "0x008506FA", "func": "FUN_008506f0", "func_entry": "0x008506F0"}],
    "14": [{"from_va": "0x00851EB5", "func": "FUN_00851e80", "func_entry": "0x00851E80"},
           {"from_va": "0x0085213B", "func": "FUN_00852110", "func_entry": "0x00852110"}],
    "17": [{"from_va": "0x00852AC9", "func": "FUN_00852a90", "func_entry": "0x00852A90"},
           {"from_va": "0x00852B38", "func": "FUN_00852b10", "func_entry": "0x00852B10"}],
    "22": [{"from_va": "0x00852BE0", "func": "FUN_00852be0", "func_entry": "0x00852BE0"},
           {"from_va": "0x00852DCF", "func": "FUN_00852dc0", "func_entry": "0x00852DC0"},
           {"from_va": "0x00852E8A", "func": "FUN_00852e00", "func_entry": "0x00852E00"}],
}

BUDGET = {
    "hash_pass_bytes_each": EXE_SIZE_PIN,
    "pe_header_bytes": 4096,
    "window_read_bytes_each": 128,
    "text_raw_bytes": 6766592,
}
BUDGET["max_total_original_bytes"] = (2 * BUDGET["hash_pass_bytes_each"] + BUDGET["pe_header_bytes"]
                                      + 2 * BUDGET["window_read_bytes_each"] + BUDGET["text_raw_bytes"])
MAX_OWN_FILES = 96
MAX_OUTPUT_BYTES = 8 * 1024 * 1024

TEXT_RAW_SIZE = 6766592
ELIGIBLE_STARTS = TEXT_RAW_SIZE - 3
CHUNK_SIZE = 1048576
CARRY = 3
MAX_HITS = 4096

EXPECTED_TEXT = {"rva": 4096, "vsize": 6764005, "rawptr": 4096, "rawsize": 6766592, "char": 0x60000020}
EXPECTED_RDATA = {"rva": 6770688, "vsize": 1009001, "rawptr": 6770688, "rawsize": 1011712, "char": 0x40000040}

LEDGER = os.path.join(OUTPUT_ROOT, "SOURCE_READS_LEDGER.jsonl")
WRITE_LEDGER = os.path.join(OUTPUT_ROOT, "WRITE_LEDGER.jsonl")
ATTEMPT_LOG = os.path.join(OUTPUT_ROOT, "ATTEMPT_LOG.jsonl")


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def jdump(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False).encode("utf-8")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            c = f.read(65536)
            if not c:
                break
            h.update(c)
    return h.hexdigest().upper()


def append_jsonl(path, obj):
    with open(path, "ab") as f:
        f.write(json.dumps(obj, ensure_ascii=False).encode("utf-8") + b"\n")


def write_new(path, data):
    if os.path.exists(path):
        raise RuntimeError("OUTPUT_COLLISION: %s already exists" % path)
    with open(path, "xb") as f:
        f.write(data)
    rsz = os.path.getsize(path)
    with open(path, "rb") as f:
        rb = f.read()
    if rb != data or len(rb) != rsz:
        raise RuntimeError("WRITE_VERIFY_FAILED: %s" % path)
    append_jsonl(WRITE_LEDGER, {"ts": utcnow(), "path": os.path.relpath(path, OUTPUT_ROOT),
                                "size": rsz, "sha256": sha256_bytes(rb), "mode": "xb"})
    return {"size": rsz, "sha256": sha256_bytes(rb)}


def write_new_text(path, text):
    return write_new(path, text.encode("utf-8"))


class BudgetExceeded(Exception):
    pass


class ShortRead(Exception):
    pass


class CentralReader(object):
    """The ONE central reader of ORIGINAL_EXE. Every read appended to the physical ledger."""

    def __init__(self):
        self.bytes_read = 0
        self.entries = []

    def load_cumulative(self):
        self.entries = self.load_ledger()
        self.bytes_read = sum(e["actual_length"] for e in self.entries)
        return self.bytes_read

    def _ledger(self, purpose, offset, requested, actual, sha, note=None):
        e = {"ts": utcnow(), "purpose": purpose, "path": EXE_PATH,
             "offset": offset, "requested_length": requested, "actual_length": actual,
             "sha256_of_read_bytes": sha, "cumulative_bytes_read": self.bytes_read}
        if note:
            e["note"] = note
        append_jsonl(LEDGER, e)
        self.entries.append(e)

    def read_at(self, offset, length, purpose):
        if self.bytes_read + length > BUDGET["max_total_original_bytes"]:
            raise BudgetExceeded("budget guard: %d+%d > %d"
                                 % (self.bytes_read, length, BUDGET["max_total_original_bytes"]))
        with open(EXE_PATH, "rb") as f:
            f.seek(offset)
            data = f.read(length)
        if len(data) != length:
            raise ShortRead("SHORT_READ: requested %d got %d at offset %d" % (length, len(data), offset))
        self.bytes_read += len(data)
        self._ledger(purpose, offset, length, len(data), sha256_bytes(data))
        return data

    def full_hash_pass(self, purpose):
        if self.bytes_read + EXE_SIZE_PIN > BUDGET["max_total_original_bytes"]:
            raise BudgetExceeded("budget guard (hash pass)")
        h = hashlib.sha256()
        n = 0
        with open(EXE_PATH, "rb") as f:
            while True:
                c = f.read(1048576)
                if not c:
                    break
                h.update(c)
                n += len(c)
        if n != EXE_SIZE_PIN:
            raise ShortRead("HASH_PASS_SIZE: %d != pin %d" % (n, EXE_SIZE_PIN))
        self.bytes_read += n
        self._ledger(purpose, 0, EXE_SIZE_PIN, n, h.hexdigest().upper(),
                     note="streaming 1 MiB chunks; single logical pass; bytes counted once")
        return h.hexdigest().upper(), n

    @staticmethod
    def load_ledger():
        entries = []
        if os.path.exists(LEDGER):
            with open(LEDGER, "rb") as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))
        return entries


def mk_patterns():
    return [(i, t, struct.pack("<I", t)) for i, t in enumerate(TARGETS)]


def scan_chunked(buf, patterns, raw_size, vsize, chunk_size, carry, max_hits):
    """Chunked scan with LOGICAL carry (carry is NOT an additional read).
    Eligible starts: 0..raw_size-4 (exclusive end raw_size-3)."""
    hits = []
    n_chunks = 0
    starts_planned = 0
    eligible_end = raw_size - 3
    for cs in range(0, raw_size, chunk_size):
        n_chunks += 1
        seg_data_end = min(cs + chunk_size + carry, raw_size)
        seg = buf[cs:seg_data_end]
        max_local_start = min(chunk_size, eligible_end - cs)
        if max_local_start <= 0:
            continue
        starts_planned += max_local_start
        for slot_index, slot_va, pat in patterns:
            pos = 0
            while True:
                idx = seg.find(pat, pos)
                if idx == -1:
                    break
                if idx < max_local_start:
                    hits.append({"slot_index": slot_index, "slot_va": "0x%08X" % slot_va,
                                 "section_offset": cs + idx})
                pos = idx + 1
    hits.sort(key=lambda h: (h["section_offset"], h["slot_index"]))
    census_complete = True
    if len(hits) > max_hits:
        hits = hits[:max_hits]
        census_complete = False
    stats = {"chunks": n_chunks, "starts_planned": starts_planned, "eligible_starts": eligible_end,
             "chunk_size": chunk_size, "carry": carry}
    return hits, census_complete, stats


def scan_unchunked(buf, patterns, raw_size):
    hits = []
    eligible_end = raw_size - 3
    for slot_index, slot_va, pat in patterns:
        pos = 0
        while True:
            idx = buf.find(pat, pos)
            if idx == -1 or idx >= eligible_end:
                break
            hits.append({"slot_index": slot_index, "slot_va": "0x%08X" % slot_va, "section_offset": idx})
            pos = idx + 1
    hits.sort(key=lambda h: (h["section_offset"], h["slot_index"]))
    return hits


def classify_span(o, vsize, rawsize):
    if o + 4 <= vsize:
        return "FULL_VIRTUAL_SPAN"
    if o < vsize:
        return "CROSSES_VIRTUAL_SIZE_END"
    if o < rawsize:
        return "RAW_PADDING_ONLY"
    return "OUT_OF_RAW"


def hit_va(o, imagebase, text_rva, text_rawptr=None):
    return imagebase + text_rva + o


def build_manifest_rows(root):
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            if rel == "MANIFEST_SHA256.csv":
                continue
            rows.append((rel, os.path.getsize(full), sha256_file(full)))
    rows.sort()
    return rows


def verify_bijection(root, manifest_path, self_excluded_name):
    problems = []
    rows = []
    with open(manifest_path, "rb") as f:
        txt = f.read().decode("utf-8")
    lines = [l for l in txt.split("\n") if l.strip()]
    header = lines[0] if lines else ""
    for l in lines[1:]:
        parts = l.split(",")
        if len(parts) != 3:
            problems.append("MALFORMED_ROW:%s" % l)
            continue
        rows.append((parts[0], int(parts[1]), parts[2].strip()))
    physical = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            physical.append(rel)
    listed = set(r[0] for r in rows)
    for rel, size, sha in rows:
        if rel.startswith("..") or "/../" in rel or "\\.." in rel:
            problems.append("PATH_TRAVERSAL_ROW:%s" % rel)
            continue
        p = os.path.join(root, rel.replace("/", "\\"))
        if not os.path.isfile(p):
            problems.append("MISSING_FILE:%s" % rel)
            continue
        if os.path.getsize(p) != size:
            problems.append("SIZE_MISMATCH:%s" % rel)
        if sha256_file(p) != sha:
            problems.append("SHA_MISMATCH:%s" % rel)
    for rel in physical:
        if rel == self_excluded_name:
            continue
        if rel not in listed:
            problems.append("UNLISTED_FILE:%s" % rel)
    return {"header": header, "rows": len(rows), "physical_files": len(physical),
            "problems": problems, "bijection_ok": (len(problems) == 0)}
