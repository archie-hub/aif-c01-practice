# aif-c01-practice

A static AIF-C01 (AWS Certified AI Practitioner) practice-exam site. The app is in `docs/` (plain HTML, CSS
and JavaScript, served by GitHub Pages from `main`); the question bank is Markdown in `aif-c01-questions/`.
It was forked from `archie-hub/saa-c03-practice` and adds ordering and matching questions. It's proxied at
`https://www.phoe.be/aif-c01-practice.html` (CloudFront behavior `/aif-c01-practice/*` in the phoe-be repo).

## Editing questions

- After changing any `aif-c01-questions/domain*.md` file, run `python3 scripts/build_questions.py` and
  commit the regenerated `docs/questions.js` with it. Never edit `docs/questions.js` by hand.
- Never renumber existing questions. Options can be freely reordered (and the correct answer's letter
  changed): each option, matching prompt and matching response has a stable id (a hash of the question id
  and its own text), and saved exam history in users' browsers refers to answers by that id. Editing an
  option's wording changes its id, which stops past exam reviews that included the old wording from being
  marked right/wrong (fine for occasional fixes, but avoid rewriting options wholesale).
- Keep options similar in length and plausible, so the correct answer can't be spotted by its length,
  and keep correct answers spread across letters. Never refer to an option by its letter in explanations:
  the app shuffles options.
- Base questions on the current exam guide
  (<https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html>) and
  only use in-scope services as correct answers. Check facts against current AWS documentation, and link a
  specific docs page in `Resource:`.
- Question types:
  - Multiple choice: `**N.** stem`, 4 options `- A.` to `- D.`, answer `**C.**`.
  - Multiple response: stem ends with `(Select TWO.)` or `(Select THREE.)`, at least 5 options, answer `**A, D.**`.
  - Ordering: `**N. (Ordering)** stem`, 3–5 steps as `- A.` options (plus optional distractor options),
    answer lists the letters in the correct order, e.g. `**C, A, D.**`. Distractors may have "why not" notes.
  - Matching: `**N. (Matching)** stem`, then 3–7 lines `- prompt => response`. A response may be reused
    across prompts. An optional `Extra choices: X | Y` line adds distractor responses. The answer block has
    no letter line: it starts with the explanation.
- Each choice question's answer block can end with a "Why not the others:" list: one `- **X.** reason` line per
  wrong option, just before `Resource:`. If a question has the list, it must cover every wrong option and no
  correct one; the build script checks this. When reordering options, move their notes' letters with them.
- An answer block can have one architecture diagram (a fenced ```` ```arch ```` block after the explanation).
  The syntax is the same as saa-c03-practice: nested boxes by indentation (`cloud`, `region`, `vpc`,
  `private`, `account`, `group`, `row`, `col`, …), icons as `id: icon Label | sub-label`, a `---` line, then
  arrows (`a -> b : label`, numbered `1. a -> b`, blocked `-x->`, dashed `~>`, both ways `<->`). A leading
  `*` on a label highlights the key piece. Icon keys are in `ARCH_ICONS` in `scripts/build_questions.py`;
  files are official AWS Architecture Icons in `docs/icons/`. Add diagrams where a flow helps (RAG, agents,
  pipelines, private connectivity), not for pure definitions.

## Editing the app

- Run `node --check docs/app.js` after changing it.
- Layouts must work at phone width (390px) without horizontal scrolling.
- Exam constants (65 questions, 90 minutes, 70% target, 700/1000 pass) are at the top of `docs/app.js`.
