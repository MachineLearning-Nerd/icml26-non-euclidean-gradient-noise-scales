import hashlib
import json
import subprocess
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = "MachineLearning-Nerd/icml26-non-euclidean-gradient-noise-scales"
FORMER_REPOSITORY = "MachineLearning-Nerd/icml26-repro-XMSaWRpEPS-non-euclidean-gradient-noise-scales"
ALLOWED_EMAILS = {
    "MachineLearning-Nerd@users.noreply.github.com",
    "37579156+MachineLearning-Nerd@users.noreply.github.com",
}
REQUIRED_FILES = {
    ".gitignore",
    "README.md",
    "STATUS.md",
    "AUTONOMOUS_STATE.json",
    "contract/live_claims.json",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "REPORT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "BRANCH_AUDIT.md",
    "branch-audit.md",
    "claims.json",
    "EVIDENCE_MANIFEST.json",
    "verify_final.py",
}


def fail(message):
    raise SystemExit("FINAL_AUDIT=FAILED " + message)


def git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        fail("git_" + args[0] + "=" + result.stderr.strip().replace("\n", " "))
    return result.stdout


def read_json(path):
    try:
        return json.loads((ROOT / path).read_text())
    except Exception as exc:
        fail("json=" + path + ":" + str(exc))


def check_sha(path, expected):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != expected:
        fail("sha=" + str(path.relative_to(ROOT)))


def check_checksum_file(path):
    for line in (ROOT / path).read_text().splitlines():
        if not line.strip():
            continue
        digest, relative = line.split(maxsplit=1)
        check_sha(ROOT / relative.strip(), digest)


head = git("rev-parse", "HEAD").strip()
local_branches = [
    line.strip()
    for line in git("for-each-ref", "--format=%(refname:short)", "refs/heads").splitlines()
]
remote_branches = [
    line.rsplit("/", 1)[-1]
    for line in git("for-each-ref", "--format=%(refname)", "refs/remotes/origin").splitlines()
    if line.rsplit("/", 1)[-1] != "HEAD"
]
if local_branches != ["main"]:
    fail("local_branches=" + repr(local_branches))
if remote_branches != ["main"]:
    fail("remote_branches=" + repr(remote_branches))
if git("for-each-ref", "--format=%(refname)", "refs/original").strip():
    fail("original_refs")

commits = [
    line.split("\t")
    for line in git("log", "--format=%H\t%an\t%ae\t%cn\t%ce\t%s", "main").splitlines()
]
if len(commits) < 4:
    fail("commit_count=" + str(len(commits)))
for record in commits:
    commit, author_name, author_email, committer_name, committer_email, subject = record
    if author_name != "MachineLearning-Nerd" or committer_name != "MachineLearning-Nerd":
        fail("commit_identity=" + commit)
    if author_email not in ALLOWED_EMAILS or committer_email not in ALLOWED_EMAILS:
        fail("commit_email=" + commit)
    if "co-authored-by:" in subject.lower():
        fail("coauthor_trailer=" + subject)

state = read_json("AUTONOMOUS_STATE.json")
if state.get("phase") != "published_and_verified":
    fail("state_phase=" + repr(state.get("phase")))
if state.get("next_action") != "select_next_icml_repository":
    fail("state_next_action=" + repr(state.get("next_action")))
if state.get("publication_allowed") is not False:
    fail("publication_allowed")
if state.get("github_repository") != "https://github.com/" + REPOSITORY:
    fail("state_repository")
if state.get("former_github_repository") != "https://github.com/" + FORMER_REPOSITORY:
    fail("state_former_repository")
if state.get("branch_set") != ["main"]:
    fail("state_branches")
if state.get("overall_verdict") != "INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY":
    fail("state_verdict")
expected_statuses = {
    "C1": "unverified",
    "C2": "unverified",
    "C3": "toy_source_norm_ratio",
    "C4": "unverified",
    "C5": "unverified",
}
if state.get("claim_statuses") != expected_statuses:
    fail("state_claim_statuses")
checkpoint = state.get("last_known_git_commit")
if not isinstance(checkpoint, str) or subprocess.run(
    ["git", "merge-base", "--is-ancestor", checkpoint, head],
    cwd=ROOT,
).returncode:
    fail("state_checkpoint_not_ancestor")

claims = read_json("claims.json")
if claims.get("repository") != REPOSITORY:
    fail("claims_repository")
if claims.get("former_repository") != FORMER_REPOSITORY:
    fail("claims_former_repository")
if claims.get("overall_verdict") != state.get("overall_verdict"):
    fail("claims_verdict")
if claims.get("publication_allowed") is not False:
    fail("claims_publication")
if claims.get("original_contract", {}).get("claim_count") != 5:
    fail("original_contract")
if [claim.get("id") for claim in claims.get("claims", [])] != ["C1", "C2", "C3", "C4", "C5"]:
    fail("claim_ids")
if {claim.get("id"): claim.get("status") for claim in claims["claims"]} != expected_statuses:
    fail("claim_status_alignment")

contract = read_json("contract/live_claims.json")
if contract.get("orid") != "XMSaWRpEPS":
    fail("claim_contract_id")
if len(contract.get("claims", [])) != 5:
    fail("claim_contract_count")

missing = sorted(name for name in REQUIRED_FILES if not (ROOT / name).is_file())
if missing:
    fail("missing_required=" + repr(missing))

check_checksum_file("evidence/source/SHA256SUMS")
check_checksum_file("outputs/claim3_norm_ratio_toy/SHA256SUMS")
check_sha(ROOT / "evidence/source/arxiv.pdf", "2894a33a0229e0193aec2f2c71e41f518251390f7de92a04e30c62cfd82506d2")
check_sha(ROOT / "evidence/source/arxiv_source.tar.gz", "5375db1a154fbebff89303c15957bdef4592eb0556c02cb8f625285e563ca5de")

with tarfile.open(ROOT / "evidence/source/arxiv_source.tar.gz") as archive:
    members = archive.getmembers()
regular_members = [member for member in members if member.isfile()]
directory_members = [member for member in members if member.isdir()]
if len(members) != 46 or len(regular_members) != 41 or len(directory_members) != 5:
    fail("source_members=" + repr((len(members), len(regular_members), len(directory_members))))
if any(member.mode & 0o111 for member in regular_members):
    fail("executable_source_member")

toy = read_json("outputs/claim3_norm_ratio_toy/summary.json")
if toy.get("l1_gns") != 0.48195497964664763:
    fail("toy_l1")
if toy.get("s1_gns") != 0.23082879701965114:
    fail("toy_s1")
if toy.get("scale7_control") != {
    "l1_gns": 0.48195497964664763,
    "s1_gns": 0.23082879701965114,
}:
    fail("toy_scale_control")
if toy.get("scope") != "toy; finite local gradients, no DDP/FSDP or Llama training":
    fail("toy_scope")

source_audit = read_json("outputs/claim1_source_audit/summary.json")
if source_audit.get("verdict") != "inconclusive":
    fail("source_audit_verdict")

readme = (ROOT / "README.md").read_text()
for phrase in ("XMSaWRpEPS", "CITATION.cff", "Thank you", "publication_allowed", "claims.json", "main", "Claim 3"):
    if phrase not in readme:
        fail("readme_phrase=" + phrase)

manifest = read_json("EVIDENCE_MANIFEST.json")
entries = manifest.get("files")
if not isinstance(entries, list):
    fail("manifest_files")
manifest_paths = [entry.get("path") for entry in entries]
if len(manifest_paths) != len(set(manifest_paths)):
    fail("manifest_duplicate")
tracked = set(filter(None, git("ls-files", "-z").split("\0")))
expected_manifest = tracked - {"AUTONOMOUS_STATE.json", "EVIDENCE_MANIFEST.json"}
if set(manifest_paths) != expected_manifest:
    fail(
        "manifest_paths_missing="
        + repr(sorted(expected_manifest - set(manifest_paths)))
        + ",extra="
        + repr(sorted(set(manifest_paths) - expected_manifest))
    )
for entry in entries:
    path = entry.get("path")
    digest = entry.get("sha256")
    if not isinstance(path, str) or not isinstance(digest, str):
        fail("manifest_entry")
    check_sha(ROOT / path, digest)

print(
    "FINAL_AUDIT=VERIFIED "
    + "branches="
    + str(len(local_branches))
    + " commits="
    + str(len(commits))
    + " claims=C1:unverified,C2:unverified,C3:toy_source_norm_ratio,C4:unverified,C5:unverified "
    + "publication_allowed=false"
)
