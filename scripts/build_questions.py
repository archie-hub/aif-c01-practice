#!/usr/bin/env python3
"""Parse aif-c01-questions/domain*.md into docs/questions.js for the web quiz.

Run from the repository root after editing any question file:

    python3 scripts/build_questions.py
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "aif-c01-questions"
OUT = ROOT / "docs" / "questions.js"
EXAM = "AIF-C01"

DOMAIN_RE = re.compile(r"^# Domain (\d): (.+?) \((\d+)%\)")
TASK_RE = re.compile(r"^## Task (\d\.\d): (.+)")
# `**12.** stem`, optionally with a tag either after the number (`**12. (Ordering)**`) or at the
# end of the stem (`… (Select TWO.)`).
QUESTION_RE = re.compile(r"^\*\*(\d+)\.(?:\s*\(([^)]+)\))?\*\*\s*(.*)")
TAG_IN_STEM_RE = re.compile(r"\s*\(((?:Select \w+|Ordering|Matching)\.?)\)\s*$")
OPTION_RE = re.compile(r"^- ([A-F])\. (.+)")
PAIR_RE = re.compile(r"^- (.+?) => (.+)$")
EXTRA_RE = re.compile(r"^Extra choices:\s*(.+)$")
ANSWER_RE = re.compile(r"^\*\*([A-F](?:,\s*[A-F])*)\.\*\*\s*(.*)")
RESOURCE_RE = re.compile(r"^Resource:\s*<([^>]+)>")
WHY_HEADER_RE = re.compile(r"^Why not the others:\s*$")
WHY_RE = re.compile(r"^- \*\*([A-F])\.\*\*\s+(.+)")
ARCH_OPEN_RE = re.compile(r"^```arch\s*$")
WORDS = {"TWO": 2, "THREE": 3}


def option_id(question_id, text):
    """Stable option identifier, independent of the option's letter/position.

    Exam history in users' browsers refers to answers by this id, so it must
    stay the same across Markdown edits that only reorder options. It changes
    only if the option's own text changes.
    """
    digest = hashlib.sha1(f"{question_id}:{text}".encode("utf-8")).hexdigest()
    return digest[:10]


def parse_tag(tag):
    """'Select TWO.' -> ('choice', 2); 'Ordering' -> ('order', None); 'Matching' -> ('match', None)."""
    tag = tag.strip().rstrip(".")
    if tag == "Ordering":
        return "order", None
    if tag == "Matching":
        return "match", None
    if m := re.fullmatch(r"Select (\w+)", tag):
        if m[1].upper() not in WORDS:
            raise ValueError(f"unknown Select count {m[1]!r}")
        return "choice", WORDS[m[1].upper()]
    raise ValueError(f"unknown tag ({tag})")


# Architecture diagrams (```arch blocks). Box kinds, outermost first in a typical nesting;
# `row` and `col` are invisible boxes that only arrange what they hold.
ARCH_BOXES = {"cloud", "onprem", "account", "region", "vpc", "az", "public", "private", "asg", "sg", "group", "row", "col"}
# Service icons: key -> (category, short label shown on the placeholder icon).
ARCH_ICONS = {
    # people, places and general resources
    "users": ("general", "Users"), "user": ("general", "User"), "internet": ("general", "Web"),
    "client": ("general", "PC"), "mobile": ("general", "Phone"), "server": ("general", "Srv"),
    "datacenter": ("general", "DC"), "firewall": ("general", "FW"),
    "document": ("general", "Doc"), "documents": ("general", "Docs"), "chat": ("general", "Chat"),
    "code": ("general", "Code"), "tool": ("general", "Tool"), "app": ("general", "App"),
    "search": ("general", "Find"), "database": ("general", "DB"), "table": ("general", "Tbl"),
    "media": ("general", "Media"), "alert": ("general", "Alrt"),
    # machine learning
    "bedrock": ("ml", "BR"), "agentcore": ("ml", "AgC"), "sagemaker": ("ml", "SM"),
    "model": ("ml", "Mdl"), "canvas": ("ml", "Cnv"), "train": ("ml", "Trn"), "notebook": ("ml", "NB"),
    "comprehend": ("ml", "Cmp"), "lex": ("ml", "Lex"), "polly": ("ml", "Ply"), "rekognition": ("ml", "Rek"),
    "textract": ("ml", "Txt"), "transcribe": ("ml", "Trs"), "translate": ("ml", "Trl"),
    "personalize": ("ml", "Per"), "q": ("ml", "Q"), "quick": ("ml", "Qk"), "nova": ("ml", "Nova"),
    "transform": ("ml", "Tfm"), "a2i": ("ml", "A2I"), "groundtruth": ("ml", "GT"), "kendra": ("ml", "Ken"),
    # compute
    "ec2": ("compute", "EC2"), "asg": ("compute", "ASG"), "lambda": ("compute", "λ"),
    "ecs": ("container", "ECS"), "eks": ("container", "EKS"), "fargate": ("container", "Fgt"),
    "ecr": ("container", "ECR"), "batch": ("compute", "Bat"), "beanstalk": ("compute", "EB"),
    "outposts": ("compute", "Out"), "localzone": ("compute", "LZ"), "wavelength": ("compute", "WL"),
    # networking
    "alb": ("network", "ALB"), "nlb": ("network", "NLB"), "gwlb": ("network", "GWLB"), "elb": ("network", "ELB"),
    "igw": ("network", "IGW"), "eigw": ("network", "EIGW"), "nat": ("network", "NAT"), "tgw": ("network", "TGW"),
    "vgw": ("network", "VGW"), "cgw": ("network", "CGW"), "vpn": ("network", "VPN"), "clientvpn": ("network", "CVPN"),
    "dx": ("network", "DX"), "dxgw": ("network", "DXGW"), "peering": ("network", "PCX"),
    "endpoint": ("network", "VPCE"), "gwendpoint": ("network", "GWE"), "privatelink": ("network", "PL"),
    "route53": ("network", "R53"), "resolver": ("network", "Rslv"), "cloudfront": ("network", "CF"),
    "accelerator": ("network", "GA"), "apigw": ("network", "API"), "lattice": ("network", "Lat"),
    "cloudwan": ("network", "WAN"), "eni": ("network", "ENI"), "nacl": ("network", "NACL"),
    "flowlogs": ("network", "Flow"), "rtb": ("network", "RT"), "networkfirewall": ("security", "NFW"),
    "verifiedaccess": ("security", "VA"),
    # storage
    "s3": ("storage", "S3"), "ebs": ("storage", "EBS"), "efs": ("storage", "EFS"), "fsx": ("storage", "FSx"),
    "glacier": ("storage", "Glac"), "storagegateway": ("storage", "SGW"), "backup": ("storage", "Bkp"),
    "snowball": ("storage", "Snow"), "instancestore": ("storage", "NVMe"), "drs": ("storage", "DRS"),
    # database
    "rds": ("database", "RDS"), "aurora": ("database", "Aur"), "dynamodb": ("database", "DDB"),
    "elasticache": ("database", "EC"), "dax": ("database", "DAX"), "memorydb": ("database", "MDB"),
    "redshift": ("analytics", "RS"), "neptune": ("database", "Nep"), "documentdb": ("database", "Doc"),
    "keyspaces": ("database", "Ksp"), "timestream": ("database", "TS"), "rdsproxy": ("database", "Prx"),
    # integration
    "sqs": ("integration", "SQS"), "sns": ("integration", "SNS"), "eventbridge": ("integration", "EvB"),
    "stepfunctions": ("integration", "SFN"), "mq": ("integration", "MQ"), "appsync": ("integration", "AS"),
    "scheduler": ("integration", "Sch"),
    # analytics
    "kinesis": ("analytics", "KDS"), "firehose": ("analytics", "Fire"), "msk": ("analytics", "MSK"),
    "athena": ("analytics", "Ath"), "glue": ("analytics", "Glue"), "emr": ("analytics", "EMR"),
    "opensearch": ("analytics", "OS"), "quicksight": ("analytics", "QS"), "lakeformation": ("analytics", "LF"),
    "databrew": ("analytics", "DB"), "dataexchange": ("analytics", "ADX"),
    "datasync": ("migration", "DS"), "dms": ("migration", "DMS"), "transfer": ("migration", "SFTP"),
    # security and identity
    "iam": ("security", "IAM"), "role": ("security", "Role"), "policy": ("security", "Pol"), "sts": ("security", "STS"),
    "identitycenter": ("security", "SSO"), "cognito": ("security", "Cog"), "directory": ("security", "AD"),
    "kms": ("security", "KMS"), "cloudhsm": ("security", "HSM"), "secrets": ("security", "SM"),
    "acm": ("security", "ACM"), "privateca": ("security", "PCA"), "waf": ("security", "WAF"),
    "shield": ("security", "Shld"), "guardduty": ("security", "GD"), "inspector": ("security", "Insp"),
    "macie": ("security", "Mac"), "securityhub": ("security", "SH"), "detective": ("security", "Det"),
    "accessanalyzer": ("security", "AA"), "firewallmanager": ("security", "FM"), "ram": ("security", "RAM"),
    "artifact": ("security", "Art"), "auditmanager": ("security", "Aud"), "dnsfirewall": ("security", "DNSF"),
    # management and cost
    "organizations": ("management", "Org"), "scp": ("management", "SCP"), "controltower": ("management", "CT"),
    "cloudtrail": ("management", "Trail"), "cloudwatch": ("management", "CW"), "config": ("management", "Cfg"),
    "ssm": ("management", "SSM"), "servicecatalog": ("management", "SC"), "trustedadvisor": ("management", "TA"),
    "computeoptimizer": ("management", "CO"), "xray": ("management", "XRay"), "fis": ("management", "FIS"),
    "resiliencehub": ("management", "RH"), "arc": ("management", "ARC"), "budgets": ("cost", "Bdgt"),
    "costexplorer": ("cost", "CE"), "savingsplans": ("cost", "SP"), "billing": ("cost", "Bill"),
}
ARCH_NODE_RE = re.compile(r"^([a-z][\w-]*):\s+([a-z0-9]+)\s+(.+)$")
ARCH_FLOW_RE = re.compile(r"^(?:(\d+)\.\s+)?([a-z][\w-]*)\s+(->|-x->|~>|<->)\s+([a-z][\w-]*)(?:\s*:\s*(.+))?$")


def parse_arch(lines):
    """Nested boxes by indentation (`vpc Label | sub`), service icons (`id: icon Label | sub`),
    then a `---` line and arrows between ids (`1. a -> b : label`; `-x->` blocked, `~>` dashed,
    `<->` both ways). A leading `*` on a label highlights the answer's key piece.
    """
    if "---" not in [l.strip() for l in lines]:
        raise ValueError("needs a --- line before the arrows")
    cut = [l.strip() for l in lines].index("---")
    root = {"c": []}
    stack = [(-1, root)]
    ids = set()
    for raw in lines[:cut]:
        indent = len(raw) - len(raw.lstrip(" "))
        text = raw.strip()
        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if "c" not in parent:
            raise ValueError(f"only boxes can contain things: {text!r}")
        if m := ARCH_NODE_RE.match(text):
            nid, icon, rest = m[1], m[2], m[3]
            if icon not in ARCH_ICONS:
                raise ValueError(f"unknown icon {icon!r}")
            if nid in ids:
                raise ValueError(f"duplicate id {nid!r}")
            ids.add(nid)
            node = {"id": nid, "i": icon}
            stack.append((indent, node))
        else:
            kind, _, rest = text.partition(" ")
            if kind not in ARCH_BOXES:
                raise ValueError(f"unknown box kind {kind!r} (or a node missing 'id: icon')")
            node = {"k": kind, "c": []}
            if m := re.search(r"\s*\[(row|col)\]$", rest):
                node["d"] = m[1]
                rest = rest[: m.start()]
            stack.append((indent, node))
        rest = rest.strip()
        if rest.startswith("*"):
            node["h"] = 1
            rest = rest[1:].strip()
        label, _, sub = rest.partition(" | ")
        if sub.strip().startswith("*"):
            raise ValueError(f"put * before the label, not the sub-label: {text!r}")
        if label.strip():
            node["n"] = label.strip()
        if sub.strip():
            node["s"] = sub.strip()
        if "k" not in node and "n" not in node:
            raise ValueError(f"icon {nid!r} needs a label")
        parent["c"].append(node)
    flows = []
    for raw in lines[cut + 1 :]:
        text = raw.strip()
        if not text:
            continue
        m = ARCH_FLOW_RE.match(text)
        if not m:
            raise ValueError(f"bad arrow {text!r}")
        for nid in (m[2], m[4]):
            if nid not in ids:
                raise ValueError(f"arrow names unknown id {nid!r}")
        flow = {"a": m[2], "b": m[4]}
        if m[1]:
            flow["no"] = int(m[1])
        if m[5]:
            if m[5].strip().startswith("*"):
                raise ValueError(f"arrow labels can't be highlighted: {text!r}")
            flow["e"] = m[5].strip()
        if m[3] != "->":
            flow["t"] = {"-x->": "x", "~>": "d", "<->": "both"}[m[3]]
        flows.append(flow)
    if not root["c"]:
        raise ValueError("empty diagram")
    return {"c": root["c"], "f": flows}


def check_choice(q):
    """Problems with a multiple-choice, multiple-response or ordering question."""
    problems = []
    letters = [o["key"] for o in q["options"]]
    if q["pairs"] or q["extra"]:
        problems.append("'=>' pairs or 'Extra choices' only belong in (Matching) questions")
    if len(set(letters)) != len(letters):
        problems.append("duplicate option letter")
    if not q["answer"]:
        problems.append("no answer")
    if len(set(q["answer"])) != len(q["answer"]):
        problems.append("answer repeats a letter")
    if any(a not in letters for a in q["answer"]):
        problems.append("answer letter not among options")
    if q["type"] == "order":
        if not 3 <= len(q["answer"]) <= 5:
            problems.append("ordering answers need 3-5 steps")
    else:
        if len(q["options"]) < (5 if q["select"] > 1 else 4):
            problems.append("too few options (4 for single answer, 5 for multiple response)")
        if q["select"] != len(q["answer"]):
            problems.append(f"select {q['select']} but {len(q['answer'])} answers")
    wrong = [k for k in letters if k not in q["answer"]]
    if any(k not in wrong for k in q["why"]):
        problems.append("'why not' note for a correct or missing option")
    if q["why"] and sorted(q["why"]) != sorted(wrong):
        problems.append("'why not' notes must cover every wrong option")
    return problems


def check_match(q):
    problems = []
    if q["options"] or q["answer"] or q["why"]:
        problems.append("matching questions use '- prompt => response' lines, not lettered options or answers")
    if not 3 <= len(q["pairs"]) <= 7:
        problems.append("matching needs 3-7 pairs")
    prompts = [p for p, _ in q["pairs"]]
    if len(set(prompts)) != len(prompts):
        problems.append("duplicate matching prompt")
    responses = {r for _, r in q["pairs"]} | set(q["extra"])
    if len(responses) < 2:
        problems.append("matching needs at least 2 different responses")
    if set(q["extra"]) & {r for _, r in q["pairs"]}:
        problems.append("an extra choice is also a correct response")
    return problems


def parse_file(path):
    domains, questions = [], []
    domain = task = q = None
    in_answer = False
    arch = None

    def finish():
        if q is None:
            return
        problems = check_match(q) if q["type"] == "match" else check_choice(q)
        if not q["resource"]:
            problems.append("no Resource: link")
        if problems:
            sys.exit(f"{path.name} {q['id']}: " + ", ".join(problems))
        if q["type"] == "match":
            pid = {p: option_id(q["id"], f"p:{p}") for p, _ in q["pairs"]}
            rid = {r: option_id(q["id"], f"r:{r}") for r in {r for _, r in q["pairs"]} | set(q["extra"])}
            q["prompts"] = [{"id": pid[p], "text": p} for p, _ in q["pairs"]]
            q["responses"] = [{"id": rid[r], "text": r} for r in sorted(rid, key=str.lower)]
            q["answer"] = [f"{pid[p]}:{rid[r]}" for p, r in q["pairs"]]
            q["select"] = len(q["pairs"])
            del q["options"]
        else:
            id_by_letter = {o["key"]: option_id(q["id"], o["text"]) for o in q["options"]}
            q["answer"] = [id_by_letter[a] for a in q["answer"]]
            q["options"] = [
                {"id": id_by_letter[o["key"]], "text": o["text"], **({"why": q["why"][o["key"]]} if o["key"] in q["why"] else {})}
                for o in q["options"]
            ]
            if q["type"] == "order":
                q["select"] = len(q["answer"])
        if q["type"] == "choice":
            del q["type"]
        for k in ("why", "pairs", "extra"):
            del q[k]
        if q["arch"] is None:
            del q["arch"]
        q["explanation"] = " ".join(q["explanation"]).strip()
        questions.append(q)

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if m := DOMAIN_RE.match(line):
            domain = {"id": int(m[1]), "name": m[2], "weight": int(m[3]), "tasks": []}
            domains.append(domain)
        elif m := TASK_RE.match(line):
            task = {"id": m[1], "name": m[2]}
            domain["tasks"].append(task)
        elif m := QUESTION_RE.match(line):
            finish()
            qid = f"{domain['id']}-{int(m[1]):02d}"
            stem, tag = m[3], m[2]
            if not tag and (s := TAG_IN_STEM_RE.search(stem)):
                tag = s[1]
                stem = stem[: s.start()]
            try:
                qtype, select = parse_tag(tag) if tag else ("choice", 1)
            except ValueError as e:
                sys.exit(f"{path.name} {qid}: {e}")
            if any(x["id"] == qid for x in questions):
                sys.exit(f"{path.name} {qid}: duplicate question number")
            q = {
                "id": qid,
                "domain": domain["id"],
                "task": task["id"],
                "type": qtype,
                "stem": stem.strip(),
                "select": select or 1,
                "options": [],
                "answer": [],
                "explanation": [],
                "resource": None,
                "why": {},
                "pairs": [],
                "extra": [],
                "arch": None,
            }
            in_answer = False
        elif q is None:
            continue
        elif arch is not None:
            if line == "```":
                if q["arch"] is not None:
                    sys.exit(f"{path.name} {q['id']}: more than one arch block")
                try:
                    q["arch"] = parse_arch(arch)
                except ValueError as e:
                    sys.exit(f"{path.name} {q['id']}: arch: {e}")
                arch = None
            elif line.startswith("</details>"):
                sys.exit(f"{path.name} {q['id']}: arch block not closed with ```")
            elif line:
                arch.append(raw.rstrip())
        elif in_answer and ARCH_OPEN_RE.match(line):
            arch = []
        elif line.startswith("<details>"):
            in_answer = True
        elif line.startswith("</details>"):
            in_answer = False
        elif not in_answer and (m := OPTION_RE.match(line)):
            q["options"].append({"key": m[1], "text": m[2]})
        elif not in_answer and (m := PAIR_RE.match(line)):
            q["pairs"].append((m[1].strip(), m[2].strip()))
        elif not in_answer and (m := EXTRA_RE.match(line)):
            q["extra"] += [x.strip() for x in m[1].split(" | ") if x.strip()]
        elif in_answer and (m := ANSWER_RE.match(line)):
            q["answer"] = [a.strip() for a in m[1].split(",")]
            if m[2]:
                q["explanation"].append(m[2])
        elif in_answer and (m := RESOURCE_RE.match(line)):
            q["resource"] = m[1]
        elif in_answer and WHY_HEADER_RE.match(line):
            continue
        elif in_answer and (m := WHY_RE.match(line)):
            if m[1] in q["why"]:
                sys.exit(f"{path.name} {q['id']}: two 'why not' notes for {m[1]}")
            q["why"][m[1]] = m[2].strip()
        elif in_answer and line:
            q["explanation"].append(line)
    finish()
    return domains, questions


def arch_nodes(items):
    for it in items:
        if "i" in it:
            yield it
        yield from arch_nodes(it.get("c", []))


def main():
    domains, questions = [], []
    for path in sorted(SRC.glob("domain*.md")):
        d, q = parse_file(path)
        domains += d
        questions += q
    used = {n["i"] for q in questions if "arch" in q for n in arch_nodes(q["arch"]["c"])}
    icons = {}
    for k in sorted(used):
        if not (ROOT / "docs" / "icons" / f"{k}.svg").exists():
            sys.exit(f"missing docs/icons/{k}.svg")
        icons[k] = {"c": ARCH_ICONS[k][0], "a": ARCH_ICONS[k][1]}
        if (ROOT / "docs" / "icons" / f"{k}-dark.svg").exists():
            icons[k]["dark"] = 1
    bank = {"exam": EXAM, "domains": domains, "icons": icons, "questions": questions}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        f"// Generated by scripts/build_questions.py from {SRC.name}/*.md. Do not edit by hand.\n"
        "window.QUESTION_BANK = " + json.dumps(bank, indent=1, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    per_domain = {d["id"]: sum(q["domain"] == d["id"] for q in questions) for d in domains}
    kinds = {}
    for q in questions:
        k = q.get("type") or ("multi" if q["select"] > 1 else "single")
        kinds[k] = kinds.get(k, 0) + 1
    diagrams = sum("arch" in q for q in questions)
    print(f"Wrote {len(questions)} questions to {OUT.relative_to(ROOT)}: {per_domain} types {kinds}, {diagrams} diagrams")


if __name__ == "__main__":
    main()
