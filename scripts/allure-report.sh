#!/usr/bin/env bash
# Builds the Allure report with trend history.
#   scripts/allure-report.sh [previous-report-dir]
# Allure 2 keeps its trends in <report>/history. Copying that folder into the new results before
# generating carries the trend forward; CI passes the report it last published to gh-pages.
# allure-pytest appends to allure-results; start a run from an empty folder for a clean report.
# The report generator is the same Allure 2 commandline the Java repositories use (it needs Java);
# it is downloaded once into .allure/ and its checksum verified.
set -euo pipefail
cd "$(dirname "$0")/.."
version=2.39.0
sha1=8ea1f552028768fefab49e1c33403cafffbf2ce8
results="allure-results"
previous="${1:-}"
if [ ! -d "$results" ]; then
  echo "allure-report: no results at $results (run a suite first)" >&2
  exit 1
fi
allure=".allure/allure-${version}/bin/allure"
if [ ! -x "$allure" ]; then
  mkdir -p .allure
  zip=".allure/allure-commandline-${version}.zip"
  curl -fsSL --retry 3 -o "$zip" \
    "https://repo1.maven.org/maven2/io/qameta/allure/allure-commandline/${version}/allure-commandline-${version}.zip"
  echo "${sha1}  ${zip}" | sha1sum -c --quiet -
  (cd .allure && unzip -q -o "allure-commandline-${version}.zip")
  chmod +x "$allure"
fi
# Allure categories mirror the family's triage categories (this lite repository has no triage
# tool; the categories are its preview).
cp config/allure/categories.json "$results/categories.json"
if [ -n "$previous" ] && [ -d "$previous/history" ]; then
  rm -rf "$results/history"
  cp -r "$previous/history" "$results/history"
  echo "allure-report: carried history from $previous"
else
  echo "allure-report: no previous history; this report starts a new trend"
fi
"$allure" generate "$results" --clean -o allure-report
echo "allure-report: allure-report/index.html"
