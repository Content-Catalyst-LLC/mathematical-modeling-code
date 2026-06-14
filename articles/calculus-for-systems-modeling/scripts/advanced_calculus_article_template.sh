#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Template: Advanced Calculus Article Companion Scaffold
#
# Copy this script for each future Calculus for Systems Modeling article.
#
# Required replacements:
#   ARTICLE_SLUG="replace-with-slug"
#   ARTICLE_TITLE="Replace With Title"
#   SEO_TITLE="Replace With SEO Title"
#
# Required standard:
#   - five-button article-map navigation in article HTML
#   - Mathematical Deepening section in article HTML
#   - advanced/ layer in repo folder
#   - convergence/error/stability/invariant checks where applicable
#   - Harvard-style Further Reading and References with authoritative links
###############################################################################

REPO_URL="git@github.com:Content-Catalyst-LLC/mathematical-modeling-code.git"
REPO_NAME="mathematical-modeling-code"
BASE_SLUG="calculus-for-systems-modeling"

ARTICLE_SLUG="replace-with-slug"
ARTICLE_TITLE="Replace With Title"
SEO_TITLE="Replace With SEO Title"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${SCRIPT_DIR}/${REPO_NAME}"
BASE_DIR="${REPO_DIR}/articles/${BASE_SLUG}"
ARTICLE_DIR="${BASE_DIR}/articles/${ARTICLE_SLUG}"

echo "Use the upgraded advanced layer from shared/advanced_standard and copy it into ${ARTICLE_DIR}/advanced."
echo "Then adapt article-specific examples, tests, references, and mathematical deepening content."
