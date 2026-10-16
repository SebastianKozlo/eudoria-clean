"""One-target RAW reference census. Importing this module performs no I/O.

Only main(), with --execute-original-read, can enter the original-read workflow.
No decoder, subprocess, network, repository operation, or implicit source search.
"""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import socket
import struct
import sys
import time
import traceback

TARGET_VA = 0x00852A30
RUN_ID = "PE_935_PARAMETER_CURSOR_CALLER_DISCOVERY_R1_20261016"
IMAGE_BASE = 0x00400000
SOURCE_SIZE = 8015872
SOURCE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
READ_BUDGET = 23814144
CHUNK_SIZE = 1024 * 1024
MAX_CANDIDATES = 4096
MAX_FILES = 32
MAX_BYTES = 8 * 1024 * 1024
REQUIRED_HOSTNAME = "WinDev2407Eval"
REQUIRED_SOURCE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
REQUIRED_OUTPUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_PARAMETER_CURSOR_CALLER_DISCOVERY_R1_20261016"
EXPECTED_SECTIONS = {
    ".text": {"virtual_size": 6764005, "rva": 4096, "raw_size": 6766592,
              "raw_pointer": 4096, "characteristics": 0x60000020},
    ".rdata": {"virtual_size": 1009001, "rva": 6770688, "raw_size": 1011712,
               "raw_pointer": 6770688, "characteristics": 0x40000040},
}
NEUTRAL_STANDING = {
    "FIELD_SEMANTICS": "UNVERIFIED_EXCEPT_SCOPED_WIDTH_AND_ADDRESS_FACTS",
    "CURSOR_SOURCE_MEDIUM": "UNKNOWN",
    "CURSOR_CONSTRUCTION_OR_FILL_UPSTREAM": "NOT_ESTABLISHED",
    "ACTUAL_ADVANCE_HELPER_EFFECTS": "NOT_ESTABLISHED",
    "ACTUAL_VIRTUAL_CALLEE_TARGET": "NOT_ESTABLISHED_UNLESS_DIRECTLY_EVIDENCED_IN_SCOPE",
    "ACTUAL_VIRTUAL_CALLEE_EFFECTS": "NOT_ESTABLISHED",
    "ALLOCATION_RETURN_EQUALS_INITIALIZATION_RETURN": "NOT_ESTABLISHED",
    "STATIC_BUILDING_ROLE": "NOT_ESTABLISHED",
    "MODEL_218757_TO_THIS_PARSER_INSTANCE": "NOT_ESTABLISHED",
    "MODEL_218757_TO_CMO_JOIN": "NOT_ESTABLISHED",
    "WORLD_INSTANCE_IDENTITY": "NOT_ESTABLISHED",
    "HISTORICAL_PLACEMENT": "NOT_ESTABLISHED",
    "WORLD_XYZ_RECOVERED": "NO",
    "PREDECESSOR_PROCESS_TERMINAL": "PARTIAL",
    "RETROACTIVE_AUTHORIZATION": "NO",
    "CANONICAL_GATE_EFFECT": "NONE",
    "REPOSITORY_MODIFIED": "NO",
    "COMMIT_PUSH": "NOT_PERFORMED",
    "EXTERNAL_POSTAUDIT_OF_THIS_RUN": "PENDING",
    "NEXT_EXPERIMENT_AUTHORIZED": "NO",
    "NEXT_MILESTONE_AUTHORIZED": "NO",
    "HARD_STOP": "YES",
}


class ScopeError(RuntimeError):
    pass


class CandidateLimitError(ScopeError):
    pass


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256(data):
    return hashlib.sha256(data).hexdigest().upper()


def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ScopeError("duplicate JSON key: " + key)
            result[key] = value
        return result
    def constant(value):
        raise ScopeError("non-finite JSON number: " + value)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def identity_bytes(data):
    return {"size_bytes": len(data), "sha256": sha256(data)}


def relative_path(value):
    if not isinstance(value, str) or "\\" in value or ":" in value:
        raise ScopeError("relative path must use plain POSIX components")
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(x in (".", "..") for x in path.parts):
        raise ScopeError("unsafe relative path: " + value)
    if str(path) != value:
        raise ScopeError("non-canonical relative path: " + value)
    return path


def is_within(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_runtime_gate(args):
    """Lexical fixed-path + local VM gate, before any path stat/open/resolve."""
    if os.name != "nt":
        raise ScopeError("original run requires Windows VM " + REQUIRED_HOSTNAME)
    source = os.path.normcase(os.path.abspath(os.fspath(args.source)))
    output = os.path.normcase(os.path.abspath(os.fspath(args.output)))
    if source != os.path.normcase(os.path.abspath(REQUIRED_SOURCE)):
        raise ScopeError("source path differs from the single contracted original")
    if output != os.path.normcase(os.path.abspath(REQUIRED_OUTPUT)):
        raise ScopeError("output path differs from the single contracted root")
    hostname = socket.gethostname()
    if hostname.casefold() != REQUIRED_HOSTNAME.casefold():
        raise ScopeError("original run requires VM hostname " + REQUIRED_HOSTNAME)
    return {"os_name": os.name, "hostname": hostname,
            "normalized_source": source, "normalized_output": output,
            "gate": "EXACT_LEXICAL_PATHS_AND_LOCAL_VM_BEFORE_FILESYSTEM_IO"}


def reject_links(path):
    """Reject symlinks/junctions in every existing path component."""
    path = Path(os.path.abspath(path))
    for item in (path, *path.parents):
        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
            raise ScopeError("symlink/junction forbidden: " + str(item))
        if os.path.lexists(item) and not item.exists():
            raise ScopeError("broken link/path forbidden: " + str(item))
    resolved = path.resolve(strict=False)
    if os.path.normcase(str(resolved)) != os.path.normcase(str(path)):
        raise ScopeError("path resolves through a redirect: " + str(path))
    return resolved


def physical_files(root):
    files = {}
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in dirs + names:
            reject_links(Path(directory) / name)
        for name in names:
            path = Path(directory) / name
            if not path.is_file():
                raise ScopeError("nonregular artifact: " + str(path))
            rel = path.relative_to(root).as_posix()
            files[rel] = path
    return files


def create_output_root(output, bundle, source):
    output, bundle, source = map(reject_links, (output, bundle, source))
    if is_within(output, bundle) or is_within(output, source.parent):
        raise ScopeError("output must be outside bundle and source parent")
    for ancestor in (output.parent, *output.parent.parents):
        if os.path.lexists(ancestor / ".git"):
            raise ScopeError("output lies inside a repository")
    if not output.parent.is_dir():
        raise ScopeError("output parent must already exist")
    # No parents=True, no exist_ok, no relocation or alternative root.
    output.mkdir()
    return output


def load_bundle(bundle, tool_path):
    bundle = reject_links(bundle)
    if not bundle.is_dir():
        raise ScopeError("bundle is not a directory")
    tool_path = reject_links(tool_path)
    if not is_within(tool_path, bundle):
        raise ScopeError("execute the frozen caller_discovery.py from its bundle")
    files = physical_files(bundle)
    manifest_name = "AUTHORING_MANIFEST_SHA256.csv"
    for name in (manifest_name, "CONTRACT.md", "INPUT_PINS.json"):
        if name not in files:
            raise ScopeError("missing bundle file: " + name)
    with files[manifest_name].open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["relative_path", "size_bytes", "sha256"]:
            raise ScopeError("authoring manifest schema mismatch")
        rows = list(reader)
    declared = {}
    for row in rows:
        rel = str(relative_path(row["relative_path"]))
        if rel == manifest_name or rel.casefold() in {x.casefold() for x in declared}:
            raise ScopeError("manifest duplicate or prohibited self row")
        declared[rel] = {"size_bytes": int(row["size_bytes"]), "sha256": row["sha256"].upper()}
    if set(declared) != set(files) - {manifest_name}:
        raise ScopeError("authoring manifest must biject all files except itself")
    for rel, expected in declared.items():
        measured = identity_bytes(files[rel].read_bytes())
        if measured != expected:
            raise ScopeError("authoring manifest identity mismatch: " + rel)
        if rel.endswith(".json"):
            strict_json(files[rel].read_text(encoding="utf-8"))
        elif rel.endswith(".jsonl"):
            for line in files[rel].read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    raise ScopeError("blank JSONL input record: " + rel)
                strict_json(line)
    pins_data = files["INPUT_PINS.json"].read_bytes()
    pins = strict_json(pins_data.decode("utf-8"))
    if not isinstance(pins, dict) or not isinstance(pins.get("files"), list):
        raise ScopeError("INPUT_PINS requires files list")
    input_ids = {}
    for pin in pins["files"]:
        rel = str(relative_path(pin["relative_path"]))
        if not rel.startswith("inputs/") or rel.casefold() in {x.casefold() for x in input_ids}:
            raise ScopeError("input path must be unique and under inputs/")
        expected = {"size_bytes": pin["size_bytes"], "sha256": pin["sha256"].upper()}
        if type(expected["size_bytes"]) is not int or expected["size_bytes"] < 0:
            raise ScopeError("input size must be a nonnegative integer")
        if rel not in declared or declared[rel] != expected:
            raise ScopeError("input pin differs from authoring manifest: " + rel)
        input_ids[rel] = expected
    if set(input_ids) != {x for x in files if x.startswith("inputs/")}:
        raise ScopeError("input pins must biject all physical input files")
    if "inputs/STANDING.json" not in input_ids:
        raise ScopeError("required pinned inputs/STANDING.json missing")
    standing = strict_json(files["inputs/STANDING.json"].read_text(encoding="utf-8"))
    if standing != NEUTRAL_STANDING:
        raise ScopeError("STANDING.json must contain the unchanged direct 22-key standing block")
    tool_rel = tool_path.relative_to(bundle).as_posix()
    if tool_rel not in declared:
        raise ScopeError("executed tool is not pinned by authoring manifest")
    copied = {"provenance/caller_discovery.py": (tool_path, declared[tool_rel]),
              "provenance/CONTRACT.md": (files["CONTRACT.md"], declared["CONTRACT.md"]),
              "provenance/INPUT_PINS.json": (files["INPUT_PINS.json"], declared["INPUT_PINS.json"]),
              "provenance/AUTHORING_MANIFEST_SHA256.csv":
                  (files[manifest_name], identity_bytes(files[manifest_name].read_bytes()))}
    for rel, ident in input_ids.items():
        copied["provenance/" + rel] = (files[rel], ident)
    # Eleven generated files plus one reserved publication-error record.
    if len(copied) + 12 > MAX_FILES:
        raise ScopeError("bundle copies leave insufficient output file budget")
    if sum(x[1]["size_bytes"] for x in copied.values()) > MAX_BYTES - 4 * 1024 * 1024:
        raise ScopeError("bundle copies leave insufficient results byte budget")
    return {"root": bundle, "copies": copied, "standing": standing,
            "contract_identity": declared["CONTRACT.md"], "tool_identity": declared[tool_rel],
            "input_pins_identity": declared["INPUT_PINS.json"]}


class ArtifactWriter:
    """Binary exclusive writes; every write verified from physical disk bytes."""
    def __init__(self, root, max_files=MAX_FILES, max_bytes=MAX_BYTES):
        self.root = root
        self.max_files = max_files
        self.max_bytes = max_bytes
        self.artifacts = {}
        self.total_bytes = 0
        self.frozen = False

    def write_bytes(self, rel, data):
        if self.frozen:
            raise ScopeError("manifest already written: no further writes")
        rel = str(relative_path(rel))
        if rel in self.artifacts or len(self.artifacts) + 1 > self.max_files:
            raise ScopeError("artifact collision or file budget exhausted")
        if self.total_bytes + len(data) > self.max_bytes:
            raise ScopeError("artifact byte budget exhausted")
        path = self.root.joinpath(*PurePosixPath(rel).parts)
        reject_links(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        expected = identity_bytes(data)
        measured = identity_bytes(path.read_bytes())
        if expected != measured:
            raise ScopeError("binary write verification failed: " + rel)
        self.artifacts[rel] = measured
        self.total_bytes += measured["size_bytes"]
        return measured

    def write_json(self, rel, payload):
        document = dict(payload)
        document["generated_utc"] = utc_now()
        document["time_provenance"] = "measured by serializer immediately before encoding/writing"
        data = (json.dumps(document, ensure_ascii=False, allow_nan=False, indent=2) + "\n").encode("utf-8")
        strict_json(data.decode("utf-8"))
        return self.write_bytes(rel, data)

    def finish_manifest(self):
        if self.frozen or "MANIFEST_SHA256.csv" in self.artifacts:
            raise ScopeError("manifest collision")
        before = physical_files(self.root)
        if set(before) != set(self.artifacts):
            raise ScopeError("untracked/missing physical artifact before manifest")
        # Strictly parse every written JSON before the last write.
        for rel, path in before.items():
            if identity_bytes(path.read_bytes()) != self.artifacts[rel]:
                raise ScopeError("artifact changed before manifest: " + rel)
            if rel.endswith(".json"):
                strict_json(path.read_text(encoding="utf-8"))
            elif rel.endswith(".jsonl"):
                for line in path.read_text(encoding="utf-8").splitlines():
                    if not line.strip():
                        raise ScopeError("blank JSONL record: " + rel)
                    strict_json(line)
        text = io.StringIO(newline="")
        writer = csv.writer(text, lineterminator="\n")
        writer.writerow(["relative_path", "size_bytes", "sha256"])
        for rel in sorted(self.artifacts):
            ident = self.artifacts[rel]
            writer.writerow([rel, ident["size_bytes"], ident["sha256"]])
        try:
            manifest_id = self.write_bytes("MANIFEST_SHA256.csv", text.getvalue().encode("utf-8"))
        finally:
            # Even a partial/failed manifest write freezes the root: recovery must
            # never append an error capture after a physically created manifest.
            self.frozen = os.path.lexists(self.root / "MANIFEST_SHA256.csv")
        # Read-only final bijection. No captures/logs/results are written afterwards.
        after = physical_files(self.root)
        if set(after) != set(self.artifacts):
            raise ScopeError("final manifest bijection failed")
        for rel, path in after.items():
            if identity_bytes(path.read_bytes()) != self.artifacts[rel]:
                raise ScopeError("read-only final rehash failed: " + rel)
        return {"manifest_identity": manifest_id, "manifest_rows": len(after) - 1,
                "physical_files": len(after), "physical_bytes": self.total_bytes,
                "bijection": "PASS_READ_ONLY", "last_write": "MANIFEST_SHA256.csv"}


class CentralOriginalReader:
    """Only content reader. Successful reads charge actual bytes, errors reserve request."""
    def __init__(self, stream, budget, source_label):
        self.stream = stream
        self.budget = budget
        self.source_label = source_label
        self.bytes_returned = 0
        self.budget_debit = 0
        self.events = []

    @classmethod
    def open_explicit_source(cls, source, execute_original_read):
        if execute_original_read is not True:
            raise ScopeError("explicit --execute-original-read required")
        return cls(Path(source).open("rb"), READ_BUDGET, str(source))

    def read_at(self, offset, count, purpose):
        if type(offset) is not int or type(count) is not int or offset < 0 or count < 0:
            raise ScopeError("invalid read interval")
        if self.budget_debit + count > self.budget:
            raise ScopeError("original-read budget would be exceeded")
        event = {"purpose": purpose, "offset": offset, "requested_bytes": count,
                 "start_utc": utc_now(), "actual_bytes": None, "status": "UNKNOWN"}
        start = time.monotonic_ns()
        try:
            self.stream.seek(offset)
            data = self.stream.read(count)
            self.bytes_returned += len(data)
            self.budget_debit += len(data)
            event.update(actual_bytes=len(data), budget_debit_bytes=len(data),
                         status="OK" if len(data) == count else "SHORT_READ")
            if len(data) != count:
                raise ScopeError("source short read at offset " + str(offset))
            return data
        except BaseException as error:
            if event["actual_bytes"] is None:
                self.budget_debit += count
                event.update(budget_debit_bytes=count, status="READ_ERROR_ACTUAL_UNKNOWN",
                             actual_bytes=None)
            event["error"] = type(error).__name__ + ": " + str(error)
            raise
        finally:
            event["end_utc"] = utc_now()
            event["elapsed_ns"] = time.monotonic_ns() - start
            self.events.append(event)

    def full_hash(self, size, purpose, chunk_size=CHUNK_SIZE):
        digest = hashlib.sha256()
        for offset in range(0, size, chunk_size):
            digest.update(self.read_at(offset, min(chunk_size, size - offset), purpose))
        return {"size_bytes": size, "sha256": digest.hexdigest().upper(),
                "hash_source": "MEASURED_BY_COUNTED_READS_NO_IDENTITY_REHASH"}


def parse_pe_header(header, source_size=SOURCE_SIZE):
    """Only parse the supplied <=4096-byte header, never follow file offsets."""
    if len(header) != 4096 or header[:2] != b"MZ":
        raise ScopeError("expected exactly 4096 bytes with MZ")
    pe = struct.unpack_from("<I", header, 0x3C)[0]
    if pe < 0x40 or pe + 24 > len(header) or header[pe:pe + 4] != b"PE\0\0":
        raise ScopeError("invalid/out-of-header PE signature")
    machine, nsections = struct.unpack_from("<HH", header, pe + 4)
    optional_size = struct.unpack_from("<H", header, pe + 20)[0]
    optional = pe + 24
    table = optional + optional_size
    if machine != 0x14C or not 1 <= nsections <= 96 or optional_size < 32:
        raise ScopeError("not bounded i386 PE32 headers")
    if table + 40 * nsections > len(header):
        raise ScopeError("section table exceeds the one header read")
    if struct.unpack_from("<H", header, optional)[0] != 0x10B:
        raise ScopeError("optional header is not PE32")
    base = struct.unpack_from("<I", header, optional + 28)[0]
    if base != IMAGE_BASE:
        raise ScopeError("ImageBase mismatch")
    sections = []
    for index in range(nsections):
        at = table + index * 40
        name = header[at:at + 8].split(b"\0", 1)[0].decode("ascii", "strict")
        virtual_size, rva, raw_size, raw_pointer = struct.unpack_from("<IIII", header, at + 8)
        characteristics = struct.unpack_from("<I", header, at + 36)[0]
        if raw_size and (raw_pointer < 4096 or raw_pointer + raw_size > source_size):
            raise ScopeError("section RAW interval outside pinned file")
        if rva + max(raw_size, virtual_size) > 0x100000000 or base + rva + virtual_size > 0x100000000:
            raise ScopeError("section virtual/raw projection wraps address space")
        sections.append({"name": name, "virtual_size": virtual_size, "rva": rva,
                         "raw_size": raw_size, "raw_pointer": raw_pointer,
                         "characteristics": characteristics})
    for left_index, left in enumerate(sections):
        for right in sections[left_index + 1:]:
            for start, length in (("raw_pointer", "raw_size"), ("rva", "virtual_size")):
                if left[length] and right[length] and max(left[start], right[start]) < min(
                        left[start] + left[length], right[start] + right[length]):
                    raise ScopeError("overlapping section intervals")
    selected = {}
    for name, expected in EXPECTED_SECTIONS.items():
        matches = [s for s in sections if s["name"] == name]
        if len(matches) != 1 or any(matches[0][key] != value for key, value in expected.items()):
            raise ScopeError("pinned section mismatch: " + name)
        selected[name] = matches[0]
    text = selected[".text"]
    if not IMAGE_BASE + text["rva"] <= TARGET_VA < IMAGE_BASE + text["rva"] + text["virtual_size"]:
        raise ScopeError("target is outside .text virtual span")
    return {"machine": "I386", "magic": "PE32", "image_base": base,
            "header_identity": identity_bytes(header), "sections": sections, "selected": selected,
            "mapping_scope": "PINNED_RAW_INTERVALS_AND_VIRTUAL_SIZE_ANNOTATIONS_ONLY"}


class Candidates:
    def __init__(self, limit=MAX_CANDIDATES):
        self.limit = limit
        self.rows = []
        self.limit_exceeded = False

    def add(self, row):
        if len(self.rows) >= self.limit:
            self.limit_exceeded = True
            raise CandidateLimitError("combined candidate cap exceeded; census incomplete")
        self.rows.append(row)


def candidate_mapping(section, offset, width):
    start = offset < section["virtual_size"]
    full = offset + width <= section["virtual_size"]
    projected_va = IMAGE_BASE + section["rva"] + offset
    return {"section": section["name"], "section_offset": offset,
            "file_offset": section["raw_pointer"] + offset,
            "raw_projected_rva": section["rva"] + offset,
            "raw_projected_site_va": "0x%08X" % projected_va,
            "site_rva": section["rva"] + offset, "site_va": "0x%08X" % projected_va,
            "site_address_model": "RAW_RVA_PROJECTION_NOT_QUALIFIED_RUNTIME_MAPPING",
            "mapped_site_va": "0x%08X" % projected_va if full else None,
            "start_within_virtual_size": start, "full_candidate_within_virtual_size": full,
            "site_in_virtual_span": start, "full_pattern_in_virtual_span": full,
            "candidate_width_bytes": width,
            "mapping_class": ("FULL_VIRTUAL_SPAN" if full else
                              "CROSSES_VIRTUAL_SIZE_END" if start else "RAW_PADDING_ONLY")}


def expected_eligible(section, mode):
    if mode == "REL32":
        return max(0, section["raw_size"] - 4)
    if mode == "POINTER32":
        first = (-section["rva"]) % 4
        return max(0, (section["raw_size"] - first - 4) // 4 + 1)
    raise ScopeError("unknown denominator channel")


def scan_section(reader, section, mode, candidates, state, chunk_size=CHUNK_SIZE):
    if mode not in ("REL32", "POINTER32") or chunk_size < 1:
        raise ScopeError("invalid bounded scan mode/chunk size")
    width = 5 if mode == "REL32" else 4
    digest = hashlib.sha256()
    carry = b""
    next_start = 0
    state.update(section=section["name"], mode=mode, raw_bytes_read=0,
                 all_candidate_starts_processed=False, completed=False,
                 expected_eligible_starts=expected_eligible(section, mode), eligible_starts_evaluated=0,
                 candidate_start_offsets_processed_through_exclusive=0)
    try:
        for position in range(0, section["raw_size"], chunk_size):
            count = min(chunk_size, section["raw_size"] - position)
            chunk = reader.read_at(section["raw_pointer"] + position, count,
                                   "SECTION_RAW_SINGLE_PASS:" + section["name"])
            digest.update(chunk)
            state["raw_bytes_read"] += len(chunk)
            data = carry + chunk
            data_start = position - len(carry)
            stop = max(0, len(data) - width + 1)
            for local in range(max(0, next_start - data_start), stop):
                offset = data_start + local
                pattern = data[local:local + width]
                match = False
                eligible = mode == "REL32" or (section["rva"] + offset) % 4 == 0
                if eligible:
                    state["eligible_starts_evaluated"] += 1
                if mode == "REL32" and pattern[0] in (0xE8, 0xE9):
                    site = IMAGE_BASE + section["rva"] + offset
                    target = (site + 5 + struct.unpack_from("<i", pattern, 1)[0]) & 0xFFFFFFFF
                    match = target == TARGET_VA
                elif mode == "POINTER32" and (section["rva"] + offset) % 4 == 0:
                    match = struct.unpack("<I", pattern)[0] == TARGET_VA
                if match:
                    row = candidate_mapping(section, offset, width)
                    row.update(raw_hex=pattern.hex(" "), target_va="0x%08X" % TARGET_VA,
                               channel="TEXT_RAW_REL32" if mode == "REL32" else "RDATA_RAW_ALIGNED_DWORD",
                               qualification_status="RAW_UNQUALIFIED",
                               raw_match_kind=("RAW_E8_REL32" if pattern[0] == 0xE8 else
                                               "RAW_E9_REL32") if mode == "REL32" else "RAW_ALIGNED_POINTER32",
                               target_arithmetic="MODULO_2_32" if mode == "REL32" else "DWORD_LE_RVA_ALIGNED_4",
                               instruction_head_status="NOT_ESTABLISHED",
                               callsite_or_function_boundary_status="NOT_ESTABLISHED",
                               caller_function_identity="NOT_ESTABLISHED",
                               producer_or_world_role="NOT_ESTABLISHED")
                    if mode == "REL32":
                        row.update(signed_disp32=struct.unpack_from("<i", pattern, 1)[0],
                                   next_va="0x%08X" % ((IMAGE_BASE + section["rva"] + offset + 5) & 0xFFFFFFFF))
                    else:
                        row.update(dword_value="0x%08X" % struct.unpack("<I", pattern)[0],
                                   site_rva_mod4=(section["rva"] + offset) % 4)
                    candidates.add(row)
                state["candidate_start_offsets_processed_through_exclusive"] = offset + 1
            next_start = max(next_start, data_start + stop)
            carry = data[-4:]
        if state["eligible_starts_evaluated"] != state["expected_eligible_starts"]:
            raise ScopeError("eligible denominator differs from actual starts evaluated")
        state.update(completed=True, all_candidate_starts_processed=True)
    finally:
        state["sha256_of_raw_bytes_read"] = digest.hexdigest().upper()
        state["hash_scope"] = ("COMPLETE_SECTION_RAW_STREAM" if state["raw_bytes_read"] == section["raw_size"]
                               else "READ_PREFIX_ONLY_NOT_COMPLETE_SECTION")


def check_candidates(rows, sections):
    """Bounded checks of stored candidate raw bytes; no new source reads/decode."""
    errors, seen = [], set()
    counts = {"TEXT_RAW_REL32": {"retained": 0, "FULL_VIRTUAL_SPAN": 0,
                                "CROSSES_VIRTUAL_SIZE_END": 0, "RAW_PADDING_ONLY": 0},
              "RDATA_RAW_ALIGNED_DWORD": {"retained": 0, "FULL_VIRTUAL_SPAN": 0,
                                           "CROSSES_VIRTUAL_SIZE_END": 0, "RAW_PADDING_ONLY": 0}}
    for index, row in enumerate(rows):
        try:
            channel = row["channel"]
            if channel not in counts:
                raise ScopeError("unknown channel")
            name, width = (".text", 5) if channel == "TEXT_RAW_REL32" else (".rdata", 4)
            section = sections[name]
            offset = row["section_offset"]
            if type(offset) is not int or not 0 <= offset <= section["raw_size"] - width:
                raise ScopeError("raw candidate outside section")
            raw = bytes.fromhex(row["raw_hex"])
            if len(raw) != width or row["qualification_status"] != "RAW_UNQUALIFIED":
                raise ScopeError("candidate raw width or qualification mismatch")
            expected = candidate_mapping(section, offset, width)
            if any(row.get(key) != value for key, value in expected.items()):
                raise ScopeError("candidate mapping/span mismatch")
            key = (channel, expected["site_rva"])
            if key in seen:
                raise ScopeError("duplicate channel/site")
            seen.add(key)
            if row["target_va"] != "0x%08X" % TARGET_VA:
                raise ScopeError("target mismatch")
            if width == 5:
                disp = int.from_bytes(raw[1:5], "little", signed=True)
                next_va = (IMAGE_BASE + section["rva"] + offset + 5) & 0xFFFFFFFF
                if raw[0] not in (0xE8, 0xE9) or (next_va + disp) & 0xFFFFFFFF != TARGET_VA:
                    raise ScopeError("rel32 candidate arithmetic mismatch")
                if row["signed_disp32"] != disp or row["next_va"] != "0x%08X" % next_va:
                    raise ScopeError("recorded displacement/nextVA mismatch")
                if row["raw_match_kind"] != ("RAW_E8_REL32" if raw[0] == 0xE8 else "RAW_E9_REL32"):
                    raise ScopeError("rel32 pattern-kind mismatch")
            elif (int.from_bytes(raw, "little") != TARGET_VA or expected["site_rva"] % 4 != 0
                  or row["site_rva_mod4"] != 0 or row["dword_value"] != "0x%08X" % TARGET_VA
                  or row["raw_match_kind"] != "RAW_ALIGNED_POINTER32"):
                raise ScopeError("DWORD/alignment mismatch")
            counts[channel]["retained"] += 1
            counts[channel][expected["mapping_class"]] += 1
        except (KeyError, ValueError, TypeError, ScopeError) as error:
            errors.append({"candidate_index": index, "error": type(error).__name__ + ": " + str(error)})
    return {"pass": not errors, "checked_rows": len(rows), "errors": errors,
            "channel_and_span_counts": counts,
            "scope": "stored raw pattern/width/target/mapping/alignment/dedup checks only; no instruction qualification"}


def post_read_checks(result, bundle, candidates, recheck, record_error):
    for rel, (path, expected) in bundle["copies"].items():
        try:
            measured = identity_bytes(path.read_bytes())
            matches = measured == expected
            recheck["files"][rel] = {"expected": expected, "measured": measured, "match": matches}
            if not matches:
                recheck["all_match"] = False
                record_error(ScopeError("saved bundle identity changed: " + str(path)), "INPUT_RECHECK")
        except Exception as error:
            recheck["all_match"] = False
            recheck["files"][rel] = {"expected": expected, "measured": None, "match": False,
                                     "error": type(error).__name__ + ": " + str(error)}
            record_error(error, "INPUT_RECHECK")
    recheck["completed"] = True
    sections = result.get("pe_mapping", {}).get("selected", {})
    result["candidate_checks"] = check_candidates(candidates.rows, sections)
    if not result["candidate_checks"]["pass"]:
        record_error(ScopeError("stored candidate QC failed"), "CANDIDATE_QC")
    result["standing_check"] = {"keys_checked": len(NEUTRAL_STANDING),
                                "exact_match": bundle["standing"] == NEUTRAL_STANDING}
    if not result["standing_check"]["exact_match"]:
        record_error(ScopeError("standing mismatch"), "STANDING_QC")


def report_polish(result):
    complete = result["census_complete"]
    lines = ["# Jednocelowy census RAW odniesień", "", "RUN_ID = " + RUN_ID,
             "PUBLICATION_STAGE = PRE_PUBLICATION (status wymaga terminalnego freeze PASS)",
             "RUN_STATUS = " + result["RUN_STATUS"],
             "SCIENCE_RESULT = " + result["SCIENCE_RESULT"], "", "Target: 0x00852A30.",
             "Zachowane kandydaty RAW: " + str(len(result["candidates"])) + ".",
             "Census zakresu RAW: " + ("ukończony" if complete else "nieukończony (PARTIAL)") + ".",
             "", "Skan obejmuje E8/E9 rel32 na każdym bajcie .text z dostępnymi 5 bajtami oraz",
             "DWORD równy targetowi na wyrównanych do 4 B RVA w .rdata. Arytmetyka rel32 jest modulo 2^32.",
             "RAW padding i pełny span w VirtualSize są jawnie rozróżnione dla każdego kandydata.",
             "Kandydat nie dowodzi głowicy instrukcji, callsite, funkcji caller, producenta kursora ani roli świata.",
             "Brak dopasowań nie dowodzi braku callerów programu; pośrednie referencje i inne encodingi są poza zakresem.",
             "Nie wykonano decode ani odczytu bodies. Nie zapisano całego EXE ani sekcji.",
             "", "SOURCE_UNCHANGED = " + result["SOURCE_UNCHANGED"],
             "Limit odczytów: 23814144 B; ledger obejmuje także pełne hashe i nagłówek.",
             "Manifest jest ostatnim zapisem. Jego fizyczny census i identity zostają zwrócone wyłącznie na stdout CLI.",
             "Log wewnętrzny nie jest capture stdout/stderr procesu systemowego.", ""]
    lines += ["Rzeczywiste oryginalne reads: " + str(result["read_totals"]["actual_bytes_returned"]) + " B;",
              "konserwatywny debit: " + str(result["read_totals"]["conservative_budget_debit_bytes"]) + " B.", ""]
    for name, channel in ((".text", "TEXT_RAW_REL32"), (".rdata", "RDATA_RAW_ALIGNED_DWORD")):
        state = result["section_streams"].get(name, {})
        counts = result["candidate_checks"]["channel_and_span_counts"][channel]
        lines += [name + ": eligible evaluated=" + str(state.get("eligible_starts_evaluated", 0))
                  + "; expected from mapping=" + str(state.get("expected_eligible_starts"))
                  + "; retained=" + str(counts["retained"])
                  + "; full span=" + str(counts["FULL_VIRTUAL_SPAN"])
                  + "; crossing=" + str(counts["CROSSES_VIRTUAL_SIZE_END"])
                  + "; raw padding=" + str(counts["RAW_PADDING_ONLY"]) + "."]
    lines += [""]
    if result["errors"]:
        lines += ["Ujawnione błędy:"] + ["- " + e["type"] + ": " + e["message"] for e in result["errors"]] + [""]
    lines += ["Standing dziedziczony z przypiętego inputs/STANDING.json:", "", "```ini"]
    lines += [key + " = " + value for key, value in result["standing"].items()]
    missing = ("kwalifikacja instruction/data reference oraz przepływu C w osobno wybranym małym oknie"
               if complete and result["candidates"] else "inne formy referencji nieobjęte dwoma kanałami"
               if complete else "ostatnia ukończona faza skanu; census pozostaje niepełny")
    lines += ["```", "", "FIRST_MISSING_EDGE = " + missing + ".",
              "HARD_STOP = YES", ""]
    return "\n".join(lines)


def run_original(args):
    if args.execute_original_read is not True:
        raise ScopeError("explicit --execute-original-read required")
    runtime_environment = validate_runtime_gate(args)
    started_utc, started_ns = utc_now(), time.monotonic_ns()
    # All frozen code/contract/input identities are measured before opening original.
    bundle = load_bundle(args.bundle, Path(__file__))
    source = reject_links(args.source)
    root = create_output_root(args.output, bundle["root"], source)
    writer = ArtifactWriter(root)
    events = []
    result = {"RUN_ID": RUN_ID, "RUN_STATUS": "PARTIAL", "SCIENCE_RESULT": "RAW_INBOUND_REFERENCE_CENSUS_PARTIAL",
              "publication_stage": "PRE_PUBLICATION",
              "run_status_authority": "effective only if CLI terminal manifest read-only verification passes; publication failure overrides to PARTIAL",
              "census_complete": False, "SOURCE_UNCHANGED": "NOT_ESTABLISHED",
              "source_path": str(source), "expected_source_identity":
                  {"size_bytes": SOURCE_SIZE, "sha256": SOURCE_SHA256},
              "target_va": "0x%08X" % TARGET_VA, "full_hashes": {}, "section_streams": {},
              "errors": [], "standing": bundle["standing"], "candidates": [],
              "total_matching_candidates": None, "original_start_utc": started_utc,
              "candidate_cap": MAX_CANDIDATES, "limit_exceeded": False,
              "qualification": "RAW_MATCHES_ONLY_NO_HEAD_CALLER_OR_PRODUCER_PROOF"}
    reader, hash1_started, scan_complete = None, False, False
    candidates = Candidates()
    phase = "COPY_PINNED_BUNDLE"
    def event(name):
        events.append({"event": name, "utc": utc_now(), "elapsed_ns": time.monotonic_ns() - started_ns})
    def record_error(error, error_phase):
        result["errors"].append({"phase": error_phase, "type": type(error).__name__,
                                 "message": str(error), "measured_utc": utc_now(),
                                 "internal_traceback": "".join(traceback.format_exception(type(error), error, error.__traceback__))
                                 if error.__traceback__ is not None else None,
                                 "traceback_status": "ACTUAL_RAISED_EXCEPTION" if error.__traceback__ is not None
                                 else "NOT_RAISED_CONSTRUCTED_ERROR"})
    try:
        for rel, (path, expected) in bundle["copies"].items():
            data = path.read_bytes()
            if identity_bytes(data) != expected:
                raise ScopeError("bundle changed before copy: " + str(path))
            if writer.write_bytes(rel, data) != expected:
                raise ScopeError("copied pin mismatch: " + rel)
        config = {"arguments": {"execute_original_read": True, "source": str(source),
                                 "output": str(root), "bundle": str(bundle["root"])},
                  "actual_argv": list(sys.argv), "python_version": sys.version, "sys_executable": sys.executable,
                  "runtime_environment": runtime_environment,
                  "tool_identity": bundle["tool_identity"], "contract_identity": bundle["contract_identity"],
                  "input_pins_identity": bundle["input_pins_identity"],
                  "limits": {"original_bytes": READ_BUDGET, "chunk_size": CHUNK_SIZE,
                             "carry_bytes": 4, "candidates_combined": MAX_CANDIDATES,
                             "own_files": MAX_FILES, "own_bytes": MAX_BYTES},
                  "attempt": "ONE_MONOLITHIC_ATTEMPT_NO_AUTOMATIC_RERUN"}
        writer.write_json("RUN_CONFIG.json", config)
        event("PINNED_BUNDLE_COPIED_AND_CONFIG_SAVED")
        phase = "OPEN_ORIGINAL"
        reader = CentralOriginalReader.open_explicit_source(source, args.execute_original_read)
        result["source_size_at_open"] = os.fstat(reader.stream.fileno()).st_size
        if result["source_size_at_open"] != SOURCE_SIZE:
            raise ScopeError("original size differs from pin")
        phase, hash1_started = "FULL_HASH_PASS_1", True
        result["full_hashes"]["pass1"] = reader.full_hash(SOURCE_SIZE, phase)
        if result["full_hashes"]["pass1"]["sha256"] != SOURCE_SHA256:
            raise ScopeError("original hash pass1 differs from pin")
        phase = "HEADER_4096"
        header = reader.read_at(0, 4096, phase)
        writer.write_bytes("HEADER4096.bin", header)
        mapping = parse_pe_header(header)
        result["pe_mapping"] = mapping
        del header
        for name, mode in ((".text", "REL32"), (".rdata", "POINTER32")):
            phase = "SCAN_RAW:" + name
            state = {}
            result["section_streams"][name] = state
            scan_section(reader, mapping["selected"][name], mode, candidates, state)
            event("SECTION_PASS_COMPLETE:" + name)
        scan_complete = True
    except Exception as error:
        record_error(error, phase)
    finally:
        if reader is not None:
            if hash1_started:
                if reader.budget_debit + SOURCE_SIZE <= reader.budget:
                    try:
                        result["source_size_before_close_hash"] = os.fstat(reader.stream.fileno()).st_size
                        result["full_hashes"]["pass2"] = reader.full_hash(SOURCE_SIZE, "FULL_HASH_PASS_2_FINALLY")
                        result["source_size_after_close_hash"] = os.fstat(reader.stream.fileno()).st_size
                    except Exception as error:
                        record_error(error, "FULL_HASH_PASS_2_FINALLY")
                else:
                    record_error(ScopeError("insufficient remaining read budget for close hash"), "FULL_HASH_PASS_2_FINALLY")
            try:
                reader.stream.close()
            except Exception as error:
                record_error(error, "CLOSE_ORIGINAL_HANDLE")
        result["candidates"] = candidates.rows
        result["limit_exceeded"] = candidates.limit_exceeded
    recheck = {"scope": "saved bundle files only, not original EXE", "files": {},
               "all_match": True, "completed": False}
    # Default records remain serializable if any post-read check throws. Source
    # reads and hashes must survive QC failures instead of becoming PREFLIGHT.
    result["candidate_checks"] = {"pass": False, "checked_rows": 0,
        "errors": [{"error": "POST_READ_QC_NOT_COMPLETED"}],
        "channel_and_span_counts": {channel: {"retained": sum(row.get("channel") == channel for row in candidates.rows),
            **{kind: sum(row.get("channel") == channel and row.get("mapping_class") == kind for row in candidates.rows)
               for kind in ("FULL_VIRTUAL_SPAN", "CROSSES_VIRTUAL_SIZE_END", "RAW_PADDING_ONLY")}}
            for channel in ("TEXT_RAW_REL32", "RDATA_RAW_ALIGNED_DWORD")}}
    result["standing_check"] = {"keys_checked": 0, "exact_match": False}
    try:
        post_read_checks(result, bundle, candidates, recheck, record_error)
    except Exception as error:
        record_error(error, "POST_READ_QC")
    hashes = result["full_hashes"]
    if (all(hashes.get(key, {}).get("sha256") == SOURCE_SHA256 for key in ("pass1", "pass2"))
            and result.get("source_size_before_close_hash") == SOURCE_SIZE
            and result.get("source_size_after_close_hash") == SOURCE_SIZE):
        result["SOURCE_UNCHANGED"] = "YES_IN_TWO_COUNTED_HASH_PASSES_AND_SIZE_CHECKS"
    if scan_complete and not result["errors"] and result["SOURCE_UNCHANGED"].startswith("YES"):
        result.update(RUN_STATUS="COMPLETE_WITHIN_BOUND", SCIENCE_RESULT="RAW_INBOUND_REFERENCE_CENSUS_COMPLETE",
                      census_complete=True, total_matching_candidates=len(candidates.rows))
    result["end_utc"] = utc_now()
    result["elapsed_ns"] = time.monotonic_ns() - started_ns
    reads = {"all_original_content_reads_via": "CentralOriginalReader", "limit_bytes": READ_BUDGET,
             "actual_bytes_returned": reader.bytes_returned if reader else 0,
             "conservative_budget_debit_bytes": reader.budget_debit if reader else 0,
             "failed_read_accounting": "requested bytes conservatively debited when returned count is unknown",
             "events": reader.events if reader else []}
    result["read_totals"] = {key: reads[key] for key in ("actual_bytes_returned", "conservative_budget_debit_bytes", "limit_bytes")}
    # Planned final outputs. If publication fails, CLI reports the concrete failure;
    # it never retries the run or overwrites an artifact already written.
    try:
        writer.write_json("READ_LOG.json", reads)
        candidate_data = "".join(json.dumps(row, ensure_ascii=False, allow_nan=False, sort_keys=True) + "\n"
                                 for row in result["candidates"]).encode("utf-8")
        candidate_identity = writer.write_bytes("CANDIDATES.jsonl", candidate_data)
        result_document = {key: value for key, value in result.items() if key != "candidates"}
        result_document["candidates_file"] = {"relative_path": "CANDIDATES.jsonl", **candidate_identity,
                                               "retained_rows": len(candidates.rows),
                                               "empty_file_means_zero_retained_rows": True}
        writer.write_json("INPUT_RECHECK.json", recheck)
        writer.write_json("RUN_RESULT.json", result_document)
        writer.write_json("INTERNAL_LOG.json", {"capture_kind": "INTERNAL_PYTHON_EVENT_LOG_NOT_OS_STDOUT_STDERR",
                                                "events": events, "errors": result["errors"]})
        writer.write_json("QC.json", {"qc_origin": "SELF_REVIEW_WITH_LIMITATIONS",
                                      "publication_stage": "PRE_PUBLICATION",
                                      "RUN_STATUS": result["RUN_STATUS"],
                                      "checked": {"source_identity_two_counted_hashes": result["SOURCE_UNCHANGED"],
                                                  "saved_input_recheck": recheck["all_match"],
                                                  "read_budget_within_limit": reads["conservative_budget_debit_bytes"] <= READ_BUDGET,
                                                  "combined_candidate_limit": len(candidates.rows) <= MAX_CANDIDATES,
                                                  "census_complete": result["census_complete"],
                                                  "candidate_arithmetic_mapping_alignment_dedup": result["candidate_checks"],
                                                  "standing_22_exact": result["standing_check"],
                                                  "denominators": result["section_streams"],
                                                  "final_physical_census": "performed by manifest final write and returned only in CLI terminal summary",
                                                  "binary_xb_disk_verification": "performed after every artifact write"},
                                      "errors": result["errors"],
                                      "limits": "no decoder, instruction-head/caller qualification, runtime, world-role proof, or independent audit"})
        writer.write_bytes("REPORT.md", report_polish(result).encode("utf-8"))
        writer.write_json("ATTEMPT.json", {"attempt": 1, "automatic_reruns": 0,
                                          "start_utc": started_utc, "end_utc": utc_now(),
                                          "RUN_STATUS": result["RUN_STATUS"], "errors": result["errors"],
                                          "capture_policy": "no fabricated OS stdout/stderr capture files"})
        manifest = writer.finish_manifest()
        return {"RUN_ID": RUN_ID, "RUN_STATUS": result["RUN_STATUS"], "SCIENCE_RESULT": result["SCIENCE_RESULT"],
                "publication_stage": "POST_MANIFEST_READ_ONLY_VERIFICATION",
                "output_root": str(root), "retained_raw_candidates": len(candidates.rows),
                "report_path": str(root / "REPORT.md"), "full_hashes": hashes,
                "channel_denominators": {name: {key: state.get(key) for key in
                    ("expected_eligible_starts", "eligible_starts_evaluated", "completed")}
                    for name, state in result["section_streams"].items()},
                "channel_and_span_counts": result["candidate_checks"]["channel_and_span_counts"],
                "census_complete": result["census_complete"], "limit_exceeded": candidates.limit_exceeded,
                "input_recheck": recheck["all_match"], "candidate_qc": result["candidate_checks"]["pass"],
                "errors": result["errors"], "standing": result["standing"],
                "total_matching_candidates": result["total_matching_candidates"],
                "original_bytes_returned": reads["actual_bytes_returned"],
                "original_budget_debit": reads["conservative_budget_debit_bytes"],
                **manifest, "HARD_STOP": "YES"}
    except Exception as error:
        # Preserve a frozen or partial root. Never write after a manifest or rerun.
        # If possible publish a small explicit publication-error record and manifest.
        recovery = {"type": type(error).__name__, "message": str(error), "utc": utc_now()}
        if not writer.frozen:
            try:
                writer.write_json("PUBLICATION_ERROR.json", {"RUN_STATUS": "PARTIAL", "error": recovery,
                                                              "original_read_ledger": reads})
                manifest = writer.finish_manifest()
                return {"RUN_STATUS": "PARTIAL", "output_root": str(root), "publication_error": recovery,
                        "original_read_ledger": reads, "full_hashes": hashes,
                        **manifest, "HARD_STOP": "YES"}
            except Exception as secondary:
                recovery["secondary_error"] = type(secondary).__name__ + ": " + str(secondary)
        return {"RUN_STATUS": "PARTIAL", "output_root": str(root), "publication_error": recovery,
                "original_read_ledger": reads, "full_hashes": hashes,
                "manifest_verification": "NOT_ESTABLISHED", "HARD_STOP": "YES"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-original-read", action="store_true")
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--bundle", required=True)
    args = parser.parse_args(argv)
    if not args.execute_original_read:
        parser.error("--execute-original-read is mandatory; no original reads performed")
    try:
        summary = run_original(args)
    except Exception as error:
        summary = {"RUN_STATUS": "BLOCKED_PREFLIGHT", "error_type": type(error).__name__,
                   "error": str(error), "original_read_workflow_not_retried": True, "HARD_STOP": "YES"}
    print(json.dumps(summary, ensure_ascii=False, allow_nan=False, indent=2))
    return 0 if summary.get("RUN_STATUS") == "COMPLETE_WITHIN_BOUND" else 1


if __name__ == "__main__":
    sys.exit(main())
