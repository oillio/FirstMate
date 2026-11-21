# Prompt: independent review

Use this prompt with a reviewer that did not write the change. For tier R, use a model family different from the author.

---

Read `AGENTS.md` and `.agents/roles/verifier.md`.

Review pull request <number or branch>. Its tier is <tier>. The requirement IDs are <IDs>.

1. Read the specification and the requirements first. Then read the tests. Then read the code.
2. For each requirement ID, find the test that proves it. List the IDs with no test.
3. Find defects. For each one, give the file and line, a concrete failure scenario (inputs and state that cause it), and the severity: blocker, major, or minor.
4. Look for these classes first: an alarm that can never fire; a stale or invalid value used as valid; replay data that can reach the live alarm path; a fallback that hides a fault; an unhandled state or error; a language model in the alarm path.
5. Run `make check`. Report the command and its output. If you cannot run it, say so.
6. Do not comment on style.

End with one line: BLOCK, CHANGES NEEDED, or NO FINDINGS.
