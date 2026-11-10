"""Checks that links in the published files lead somewhere a reader can go.

This repository is the public source snapshot. The project's original
repository, github.com/muhib-karim/Rambler-Bangla, is private, so a link to it
is a 404 for everyone else. Links must use muhib-karim/Rambler-Bangla-Public.
The Pages site, muhib-karim.github.io/Rambler-Bangla/, is public and allowed.

Needs only Python 3 (stdlib unittest); uses git to list tracked files when
it can.
    python3 -m unittest discover -s tests/python -v
"""
import os
import re
import subprocess
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# File types whose links readers follow. Python sources are left out on
# purpose: this file has to spell the private URL to test the detector.
LINKED_SUFFIXES = (".md", ".yml", ".yaml", ".html")

# The private repository on any GitHub host (github.com, api.github.com/repos,
# raw.githubusercontent.com), or a shields.io badge that reads from it. The
# lookahead lets "Rambler-Bangla-Public" through.
PRIVATE_REPO = re.compile(
    r"(?:github(?:usercontent)?\.com/(?:repos/)?"
    r"|img\.shields\.io/github/[^\s\"'()<>]*?/)"
    r"muhib-karim/Rambler-Bangla(?!-Public)"
)

# Markdown links and images, plus the HTML attributes the README uses.
LINK = re.compile(r"\]\(([^)\s]+)\)|(?:href|src)=\"([^\"]+)\"")

# Only used when git cannot list the files (for example a zip download).
UNTRACKED_DIRS = {".git", "tools", "build", "__pycache__"}


def private_repo_links(text):
    """Every reference to the private repository found in text."""
    return PRIVATE_REPO.findall(text)


def tracked_files():
    """Repository-relative paths of the files git tracks."""
    try:
        listing = subprocess.run(["git", "-C", ROOT, "ls-files", "-z"],
                                 capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        found = []
        for folder, dirs, names in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in UNTRACKED_DIRS]
            found += [os.path.relpath(os.path.join(folder, n), ROOT) for n in names]
        return sorted(p.replace(os.sep, "/") for p in found)
    return [p for p in listing.decode("utf-8").split("\0") if p]


def numbered_lines(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return list(enumerate(fh.read().splitlines(), 1))


class PublicLinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = [p for p in tracked_files() if os.path.isfile(os.path.join(ROOT, p))]

    def test_detector_tells_the_private_repo_from_the_public_one(self):
        private = (
            "https://github.com/muhib-karim/Rambler-Bangla",
            "https://github.com/muhib-karim/Rambler-Bangla/issues/new/choose",
            "git clone https://github.com/muhib-karim/Rambler-Bangla.git",
            "[README](https://github.com/muhib-karim/Rambler-Bangla#build-from-source)",
            '<a href="https://github.com/muhib-karim/Rambler-Bangla">GitHub</a>',
            "https://img.shields.io/github/v/release/muhib-karim/Rambler-Bangla",
            "https://raw.githubusercontent.com/muhib-karim/Rambler-Bangla/main/README.md",
            "https://api.github.com/repos/muhib-karim/Rambler-Bangla/releases",
        )
        public = (
            "https://github.com/muhib-karim/Rambler-Bangla-Public",
            "https://github.com/muhib-karim/Rambler-Bangla-Public/issues/new/choose",
            "git clone https://github.com/muhib-karim/Rambler-Bangla-Public.git",
            "https://img.shields.io/github/license/muhib-karim/Rambler-Bangla-Public",
            "https://muhib-karim.github.io/Rambler-Bangla/",
            "https://muhib-karim.github.io/Rambler-Bangla/assets/1-banner.png",
            "https://github.com/muhib-karim",
        )
        for text in private:
            self.assertTrue(private_repo_links(text), f"should be caught: {text}")
        for text in public:
            self.assertFalse(private_repo_links(text), f"should be allowed: {text}")

    def test_no_link_to_the_private_repository(self):
        scanned = [p for p in self.files if p.endswith(LINKED_SUFFIXES)]
        self.assertIn("README.md", scanned, "the file listing is empty or wrong")
        hits = [f"{path}:{number}: {line.strip()[:120]}"
                for path in scanned
                for number, line in numbered_lines(path)
                if private_repo_links(line)]
        self.assertEqual(hits, [], "these link to the private repository; "
                                   "use muhib-karim/Rambler-Bangla-Public")

    def test_relative_links_in_markdown_resolve(self):
        missing = []
        for path in (p for p in self.files if p.endswith(".md")):
            folder = os.path.join(ROOT, os.path.dirname(path))
            for number, line in numbered_lines(path):
                for groups in LINK.findall(line):
                    link = groups[0] or groups[1]
                    if link.startswith(("http://", "https://", "mailto:", "#", "data:")):
                        continue
                    target = link.split("#", 1)[0]
                    if target and not os.path.exists(os.path.join(folder, target)):
                        missing.append(f"{path}:{number}: {link}")
        self.assertEqual(missing, [], "these point at files that are not in the repository")


if __name__ == "__main__":
    unittest.main()
