# Changelog

All notable changes to Rambler Bangla. Dates are AEST/AEDT. Test builds are maintainer builds, not public downloads; see the README section "Source only, no APKs".

## Public snapshot housekeeping - 2026-11-10

Repository housekeeping for the public source snapshot. No patcher behaviour, runtime, fingerprint or signing changes, and no APKs.

- CI (`ci.yml`) gates pull requests with the Python unit tests on Python 3.11 and 3.12, ruff and a gitleaks secret scan, with every action pinned to a commit SHA. The static-suite job is gone from CI because `tests/run_tests.sh` and `tools-src/` are not part of this snapshot. `tests.yml` is manual-only, says so in its first step, and gates on the exact `TEST SUITE: N passed, 0 failed` line.
- New `pyproject.toml` with a small ruff configuration. Lint fixes with no behaviour change: unused imports and a dead variable in `fixtures/build_fixture.py`, `rename/rename_apk.py` and `scripts/clip_e2e.py`, and an unused loop variable in `standalone-patcher/dex_patch.py`.
- Links in the README, docs, site page and community files point at this repository instead of the private original. Release links go to the changelog and release notes, because no release has been published here. Links to files that are not in the snapshot are plain text. The two CI-run URLs in `ledger/` keep their run ids as text.
- README: new "What's here" section, and CI and licence badges for this repository. The release and static-suite badges are gone.
- Removed three duplicated `.github/` trees that GitHub never read.

## V29.5 - 2026-10-24 (in review, not released)

Clipboard Recent | History. Static and host-tested only: no phone or emulator has run this build yet. It is an overlay on the maintainer's V29.4 rc4 build, not a published release.

- The clipboard panel gets a small Recent | History tab row above the clip list. Recent is the stock list, unchanged; ClipOrder, ClipDrag, ClipSmooth and ClipAccess still act on it. History is a scrolling list of the last 50 unique text clips, newest first, above up to 10 pinned clips that do not count towards the 50. Copying the same text again moves it to the top. Tap pastes into the current field; long-press offers Pin or Unpin and Delete.
- History survives keyboard restarts. It lives in one app-private file in the no-backup directory, written atomically, and is never read before the phone is first unlocked. No network code.
- Recording rides on Gboard's own clipboard read, so it works while the panel is closed. It only records live copies (clipboard timestamp within 10 seconds) of plain text up to 32,768 characters. It skips clips marked `IS_SENSITIVE`, clips Gboard masks, Gboard incognito, clipboard opt-in off, and copies made while a password or no-learning field is active, even if focus moves on before the read is handled. Deleting an entry leaves no copy or hash of its text. History is hidden in those fields too.
- New runtime classes in `extension-src/.../rambler/` (`GboardRamblerClipHistory`, `ClipHistoryPanel`, `ClipHistoryStore`, `ClipHistoryPolicy`, `ClipHistoryGboardPrivacy`). Seven hook calls in seven Gboard methods, each pinned by method hash in `fingerprints/clipboard-history-rc4.json`: IME start, finish and destroy (`aeij`), the clipboard read (`kvk.call`), and panel open, close and view discard (`ClipboardKeyboard`).
- `scripts/build_clip_history.sh BASE OUTPUT` refuses anything but the exact rc4 APK. It checks every hooked method's hash and anchor, that every hook calls an existing runtime method with the right number of arguments, and that every Gboard name the runtime reaches by reflection exists. It also checks that untouched classes and APK entries are unchanged. It adds the runtime as `classes6.dex` and writes an unsigned, zipaligned APK. No resource or manifest changes.
- 9 new Python unit tests (49 in total), including a JVM harness for the store and privacy policy, and synthetic hook, guard and ZIP fixtures.

## [29.4.1] - 2026-10-21

Docs only. No patcher, runtime, fingerprint or signing changes, and no APKs.

- README rewritten as the project homepage: what and why, architecture mermaid (fingerprint guard, smali patch, policy runtime, verify), device-free CI, build from source, fail-closed safety, source-only and legal note, FAQ, roadmap and links. Latest release now points at v29.4.
- GitHub Pages landing page restyled to match: mobile-first, WCAG AA colour tokens, skip link and landmarks, native FAQ, no scripts, external fonts or trackers.
- New stdlib unit tests (`tests/python/test_docs_homepage.py`) keep the README and the site honest: required sections, badges, local links, quoted test count, contrast, no trackers. The CI unit job now runs 40 tests.
- CI: `ci.yml` bumps `actions/checkout` 4 to 7, `actions/setup-python` 5 to 7 and `actions/setup-java` 4 to 6 (Dependabot #15, #17, #16).
- Docs index lists the V29.4 release notes.

## V29.4 - 2026-10-18

Source-only release. No runtime or conversion changes against V29.3. Details: [`docs/V29.4-RELEASE-NOTES.md`](docs/V29.4-RELEASE-NOTES.md).

- New maintainer signing key (certificate SHA-256 `679cfdec...2e78`); the V29.3 key is lost. Builds signed with the new key cannot install over V29.3 builds: uninstall once first. Record: [`ledger/v29.4-provenance.md`](ledger/v29.4-provenance.md).
- The maintainer key now lives only in GitHub Actions secrets (plus an offline backup kept by the maintainer). New manual workflow `maintainer-key-check.yml` signs the synthetic fixture with it and checks the signer; it publishes no APK.
- Docs: portfolio README, architecture, user guide and releasing docs, docs index; community files (code of conduct, contributing, PR and issue templates, CODEOWNERS, Dependabot).
- CI: `ci.yml` runs 26 Python unit tests for the patcher helpers and the static suite on every push and pull request.
- Patcher fix: array parameters count as one register slot in `dex_patch.py`, whatever the element type.
- Project website (GitHub Pages), banner, brand sheet, icon showcase and favicon (2026-10-05 to 2026-10-08).
- Fixture hygiene: personal-looking emails in the v29.3 corpus, target and golden fixtures replaced with `example.com` addresses.
- Removed the temporary clipboard-mask and instrumented-settings diagnostic probes and their workflows.
- Dependency bumps: `actions/checkout` 4.2.2 to 7.0.1, `actions/upload-artifact` 4.6.2 to 7.0.2.

### Maintainer test builds 245 to 253 - October 2026

Private builds, not public downloads, and not part of this source release. Evidence levels in the README's "Maintainer builds, October 2026" table.

- 253: compatibility update, two static reviews passed; the maintainer reports the Gboard AI writing-tools icon is back on their phone. Cause not proven.
- 251: removes the pin exemption for the stray "123" label (static review; phone check pending).
- 250: unpinned path clean on the phone; pinned still showed "123".
- 247 to 249: spacebar label and list/popup candidates; not shipped.
- Planned: clause segmentation, phonetic typing with EN/BN toggle, Bangla (Latin).

## V29.3 - 2026-09-24

- One language per sentence in multilingual voice typing.
- Real Bangla spellings for English words (CMU Pronouncing Dictionary plus reviewed overrides).
- Protected text: #hashtags, @handles, links, emails and times stay in Latin letters.
- Clipboard drag-to-reorder (in development).
- Host corpus of 292 cases passes all gates. Details: [`docs/V29.3-RELEASE-NOTES.md`](docs/V29.3-RELEASE-NOTES.md).

## V29 - 2026-09-23

- Bangla spelling normalization: garble-resistant English near-match demotion and a 2,265-pair roman-to-script table.
- Design: [`docs/V29-DESIGN.md`](docs/V29-DESIGN.md).

## V28 / v28d

- Segment-locked multilingual dictation. Last stable baseline. Evidence: [`docs/EVIDENCE.md`](docs/EVIDENCE.md).
