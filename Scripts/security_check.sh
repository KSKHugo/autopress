#!/bin/bash
# Security check before anything reaches GitHub — run by the pre-push hook on this
# Mac and by .github/workflows/security.yml on GitHub. Fails on any finding.
#
#   1. gitleaks     secrets (keys, tokens, passwords) in every commit of the history
#   2. osv-scanner  known vulnerabilities in dependencies, should any lock file appear
#   3. semgrep      code patterns: the Python build scripts, the local preview server,
#                   shell, workflows, Swift helpers, secrets
#
# This repository is public: GitHub's CodeQL and secret scanning run on it as well.
#
# Install on the Mac: brew install gitleaks osv-scanner semgrep
#
# A finding that is not a vulnerability is marked where it occurs, with the reason:
# `# nosemgrep: <rule>` for semgrep, `gitleaks:allow` for gitleaks.
set -u
cd "$(dirname "$0")/.."

failed=0
step() { printf '\n== %s\n' "$1"; }
need() {
    command -v "$1" >/dev/null || { echo "missing tool: $1 (brew install $1)"; exit 2; }
}
need gitleaks; need osv-scanner; need semgrep

step "Secrets in the history (gitleaks)"
gitleaks git --log-opts="--all" --redact --no-banner . || failed=1

step "Known vulnerabilities in dependencies (osv-scanner)"
lockfiles=()
while IFS= read -r file; do lockfiles+=(-L "$file"); done < <(git ls-files '*Package.resolved')
if [ ${#lockfiles[@]} -gt 0 ]; then
    osv-scanner scan source "${lockfiles[@]}" || failed=1
else
    echo "no Package.resolved"
fi

step "Code patterns (semgrep)"
# Only what git tracks: build output (dist/, caches) is not part of it.
files=()
while IFS= read -r file; do files+=("$file"); done < <(git ls-files '*.swift' '*.py' '*.sh' '*.yml' '*.yaml' '*.plist' '*.entitlements' '*.json' '*.js')
semgrep scan --metrics=off --quiet --error \
    --config p/swift --config p/secrets --config p/python --config p/github-actions \
    --config p/javascript \
    "${files[@]}" || failed=1

if [ "$failed" -ne 0 ]; then
    printf '\nSECURITY CHECK FAILED — nothing should be pushed until the findings above are fixed or explained.\n'
    exit 1
fi
printf '\nSecurity check passed.\n'
