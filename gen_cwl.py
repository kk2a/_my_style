from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STY_FILE = ROOT / "_my_style.sty"
CWL_FILE = ROOT / "_my_style.cwl"

COMMAND_PATTERN = re.compile(r"\\newcommand\{\\([^@]\w*)\}(?:\[(\d+)\])?\{")
INPUT_PATTERN = re.compile(r"\\(?:input|include)\{([^}]+)\}")
ENVIRONMENT_PATTERNS = (
    re.compile(r"\\newenvironment\{(\w+)\}"),
    re.compile(r"\\NewDocumentEnvironment\{(\w+)\}"),
    re.compile(r"\\newtheorem\*?\{(\w+)\}"),
)


def format_command(name, arg_count):
    args = "".join(f"{{arg{index}}}" for index in range(1, int(arg_count or 0) + 1))
    return f"\\{name}{args}"


def format_environment(name):
    return f"\\begin{{{name}}}\n\\end{{{name}}}"


def append_unique(items, item):
    if item not in items:
        items.append(item)


def resolve_input_path(parent, input_name):
    input_path = (parent / input_name).resolve()
    candidates = [input_path]
    if input_path.suffix == "":
        candidates.append(input_path.with_suffix(".sty"))

    for candidate in candidates:
        if candidate.is_file() and ROOT in candidate.parents:
            return candidate
    return None


def extract_cwl_entries(file_path, seen=None):
    seen = seen or set()
    file_path = file_path.resolve()
    if file_path in seen:
        return []
    seen.add(file_path)

    commands = []
    environments = []

    for line in file_path.read_text(encoding="utf-8").splitlines():
        input_match = INPUT_PATTERN.match(line)
        if input_match:
            input_path = resolve_input_path(file_path.parent, input_match.group(1))
            if input_path:
                for entry in extract_cwl_entries(input_path, seen):
                    append_unique(commands, entry)
            continue

        command_match = COMMAND_PATTERN.match(line)
        if command_match:
            append_unique(commands, format_command(*command_match.groups()))
            continue

        for pattern in ENVIRONMENT_PATTERNS:
            environment_match = pattern.match(line)
            if environment_match:
                append_unique(environments, format_environment(environment_match.group(1)))
                break

    return commands + environments


def write_cwl(entries, output_path):
    output_path.write_text("\n".join(entries) + "\n", encoding="utf-8")


if __name__ == "__main__":
    entries = extract_cwl_entries(STY_FILE)
    write_cwl(entries, CWL_FILE)
    print(f"Generated {CWL_FILE.name} from {STY_FILE.name}")