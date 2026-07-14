"""
SOP Feedback Tool
------------------
Gives structured, criteria-based feedback on a draft Statement of Purpose (SOP),
built to support Maryam's mentorship practice helping women prepare graduate
school applications abroad.

Usage:
    export ANTHROPIC_API_KEY="your-key-here"
    python sop_feedback_tool.py path/to/sop_draft.txt
    python sop_feedback_tool.py path/to/sop_draft.txt --program "MSc Computer Science, TU Delft"

Output:
    Writes a feedback report to <input_filename>_feedback.md in the same folder,
    and also prints it to the terminal.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import anthropic

MODEL = "claude-sonnet-5"

FEEDBACK_CRITERIA = """
Evaluate the SOP against these six criteria. For each one, give a short
assessment (3-5 sentences) plus one concrete suggestion for improvement.
Do not rewrite the SOP for the applicant, coach them on what to fix
themselves, the way a mentor would in a one-on-one session.

1. Opening & hook - Does the first paragraph include basic introduction of the applicant?
   name, degree (including the major and the year of graduation)?
   does the rest of the first paragraph earn attention, or does it open
   with a generic statement ("Since childhood, I have been passionate about...")?
2. Narrative arc - Does the SOP tell a coherent story connecting past
   experience to the specific program, or does it read as a list of
   accomplishments with no throughline?
3. Specificity & evidence - Are claims backed by concrete examples (projects,
   courses, results), or are they vague assertions ("I am a hard worker")?
4. Fit with the specific program - Does the applicant explain *why this
   program, this department, these faculty* rather than a generic case for
   the field? Flag any place where the program name could be swapped out
   without the paragraph changing.
5. Structure & flow - Is there a clear beginning (motivation), middle
   (relevant background/evidence), and end (specific future goals tied back
   to the program)? Note any paragraphs that feel out of order or redundant.
6. Language & tone - Flag any phrasing that is overly informal, overly
   flowery/cliched, or grammatically unclear. Note English is clearly not
   the writer's first language in a way that could distract a reviewer, and
   suggest specific fixes rather than general "polish this" comments.

Finish with a short "Top 3 priorities" section - the three highest-impact
changes the applicant should make first, ordered by importance.
"""


def load_sop(path: Path) -> str:
    if not path.exists():
        sys.exit(f"Error: file not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        sys.exit(f"Error: file is empty: {path}")
    return text


def build_prompt(sop_text: str, program: str | None) -> str:
    program_line = f"\nTarget program: {program}\n" if program else (
        "\nNo target program was specified -- evaluate criterion 4 (fit) "
        "generally, and note that program-specific feedback would sharpen "
        "the review further.\n"
    )
    return (
        f"Here is a draft Statement of Purpose for a graduate school application."
        f"{program_line}\n"
        f"--- SOP DRAFT START ---\n{sop_text}\n--- SOP DRAFT END ---\n\n"
        f"{FEEDBACK_CRITERIA}"
    )


def get_feedback(client: anthropic.Anthropic, sop_text: str, program: str | None) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=(
            "You are an experienced graduate admissions mentor who has helped "
            "many first-generation and international applicants prepare "
            "Statements of Purpose. You are direct, specific, and encouraging, "
            "but you never sugarcoat weak spots. You coach rather than rewrite."
        ),
        messages=[{"role": "user", "content": build_prompt(sop_text, program)}],
    )
    return "".join(block.text for block in message.content if block.type == "text")


def main():
    parser = argparse.ArgumentParser(description="Get structured feedback on a draft SOP.")
    parser.add_argument("sop_file", type=Path, help="Path to a .txt file containing the SOP draft")
    parser.add_argument("--program", type=str, default=None, help="Target program name, e.g. 'MSc Computer Science, TU Delft'")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit(
            "Error: ANTHROPIC_API_KEY is not set.\n"
            "Set it first, e.g.:\n"
            '    export ANTHROPIC_API_KEY="your-key-here"   (Mac/Linux)\n'
            '    setx ANTHROPIC_API_KEY "your-key-here"      (Windows)\n'
            "Get a key at https://console.anthropic.com/settings/keys"
        )

    sop_text = load_sop(args.sop_file)
    client = anthropic.Anthropic()

    print("Getting feedback... (this takes 10-20 seconds)\n")
    try:
        feedback = get_feedback(client, sop_text, args.program)
    except anthropic.APIError as e:
        sys.exit(f"API error: {e}")
    except Exception as e:
        sys.exit(f"Unexpected error: {e}")

    out_path = args.sop_file.with_name(args.sop_file.stem + "_feedback.md")
    header = (
        f"# SOP Feedback\n\n"
        f"Source file: {args.sop_file.name}  \n"
        f"Program: {args.program or 'not specified'}  \n"
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n"
    )
    out_path.write_text(header + feedback, encoding="utf-8")

    print(feedback)
    print(f"\n\nSaved to {out_path}")


if __name__ == "__main__":
    main()
