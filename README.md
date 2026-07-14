# SOP Feedback Tool

A command-line tool that gives structured, criteria-based feedback on draft
graduate school Statements of Purpose (SOPs), built with the Claude API.

## Why I built this

For several years I've informally mentored women pursuing graduate study
abroad — helping them rework resumes, refine SOPs, and find affordable
programs. Evaluating SOP is time-consuming and be automated using an AI tool.

This tool doesn't replace that mentoring — it handles the first, most
repetitive pass, so my own time goes toward the judgment calls a script
can't make: how a specific person's story should be framed, what's true to
their voice, what risks are worth taking in a given application.

## What it does

Given a draft SOP (and optionally a target program name), it evaluates the
draft against six criteria a strong SOP needs to satisfy:

1. **Opening & hook** — does it earn attention, or open generically?
2. **Narrative arc** — is there a coherent throughline, or a list of achievements?
3. **Specificity & evidence** — concrete examples, or vague claims?
4. **Fit with the specific program** — real specificity, or a swappable paragraph?
5. **Structure & flow** — clear beginning/middle/end?
6. **Language & tone** — clarity issues, cliché, awkward phrasing?

It closes with a **Top 3 priorities** list — the highest-impact fixes to make
first — because a mentee facing 20 pieces of feedback at once tends to act on
none of them.

It's deliberately built to *coach*, not rewrite: the system prompt explicitly
instructs the model not to generate replacement text, since the point is to
help someone improve their own writing, not hand them someone else's.

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-key-here"   # from console.anthropic.com/settings/keys
```

## Usage

```bash
python sop_feedback_tool.py draft.txt
python sop_feedback_tool.py draft.txt --program "MSc Data Science, OU"
```

Feedback prints to the terminal and is saved as `draft_feedback.md` alongside
the input file.

## Example

`example_input.txt` is a deliberately generic, synthetic SOP opening (not a
real applicant's material) written to show the kind of vague, unspecific
writing the tool is designed to catch — a generic hook, unearned claims
("hard worker," "world-class faculty"), and no concrete evidence.

Run it yourself to see the tool in action:

```bash
python sop_feedback_tool.py example_input.txt
```

This generates `example_input_feedback.md` — commit that file too once you've
run it, so a reviewer can see real tool output without needing their own API key.

## How this was built

I designed the tool's approach, the feedback criteria, 
the constraints that the tool should give suggestions rather than rewrite the SOP,
, and what a first pass review should look like. 
I built the Python implementation using Claude to generate the initial code,
then tested and adjusted it myself. 
I tested this version against real and synthetic SOP drafts before relying on it.

## Stack

Python, Anthropic API (Claude)
