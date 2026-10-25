# aif-c01-practice

## AIF-C01 practice exams

A static web app for practicing the AWS Certified AI Practitioner (AIF-C01) exam, built on exam guide
version 1.1 (April 2026), which added agentic AI, MCP, Amazon Bedrock AgentCore, Kiro, Strands Agents,
Amazon Quick, context engineering, and other new objectives. It lives in [`docs/`](docs/) and runs on
GitHub Pages with no server. It's also served at <https://www.phoe.be/aif-c01-practice.html>.

- **65-question exams** weighted by domain like the real exam (D1 20%, D2 24%, D3 28%, D4 14%, D5 14%),
  with an optional 90-minute timer. Exams start in study mode (check each answer as you go); switch to exam
  mode to see your score only at the end. You can also choose a single domain or a different length.
- **All four question types from the real exam**: multiple choice, multiple response, **ordering** (tap the
  steps first to last) and **matching** (pick a response for each item).
- **A different exam each time.** *Balanced* mode draws the questions you've seen least, so successive exams
  rotate through the whole bank. *Weak spots* puts your recently missed questions first. *Random* is a plain
  shuffle. Answer options are shuffled on every run.
- **Explanations** for every question, a note on why each wrong option is wrong, an architecture diagram where
  one helps, and a link to the AWS documentation page to study.
- **Run tracking.** Every finished exam is saved with your answers, time taken, and per-domain and per-task scores.
  You can review any past exam question by question, or retake just the ones you missed.
- **Progress dashboard.** A score trend across exams, accuracy by domain and task against a 70% target,
  and coverage of the question bank.

Progress is stored in your browser's `localStorage`, so it's per browser and per device (and separate for
github.io and phoe.be). Use **History → Export / Import** to back it up or move it to another device.

### Run locally

```sh
cd docs && python3 -m http.server 8000
# open http://localhost:8000
```

Opening `docs/index.html` directly from disk also works.

### Adding or editing questions

The question bank is written in Markdown in [`aif-c01-questions/`](aif-c01-questions/). After changing it,
regenerate the data file the site loads and commit both:

```sh
python3 scripts/build_questions.py   # writes docs/questions.js
```

The script checks every question's options, answers, "why not" notes, ordering and matching structure,
resource link and diagram. See [`CLAUDE.md`](CLAUDE.md) for the full format.
