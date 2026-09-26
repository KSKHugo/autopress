#!/bin/zsh
# Prepares the work folder for the website screenshots (outside OneDrive):
#   demo/     the drawn pictures, the WordPress mock, winid
#   l10n/     the scripts and tools, and per language the demo folder + terms
#   shots/    where mac.sh and ios.sh write, one folder per language
# Then: l10n/mac.sh <lang>   (Mac, fully automatic; ONLY="main done" for a part)
#       l10n/ios.sh <lang> prep|detail|crop|rest|schedule|done   (two taps by hand:
#       "Crop…" in the post after "detail", the Scheduled segment at 313,335 after "rest")
# Needs Debug builds of the app in ~/Library/Caches/AutoPress-DerivedData (macOS and
# iOS simulator). Copy the results into assets/img/<lang>/ as described in the README.
set -e
HERE=${0:A:h}
S="${AUTOPRESS_SHOTS:-$HOME/Library/Caches/AutoPress-Shots}"
mkdir -p "$S/demo/Coastline Journal/images" "$S/l10n" "$S/shots"
cp "$HERE"/mock.py "$HERE"/winid.swift "$S/demo/"
cp "$HERE"/demo.py "$HERE"/mac.sh "$HERE"/ios.sh "$S/l10n/"
(cd "$S/demo" && swift "$HERE/draw.swift" && mv "Coastline Journal/alfama-rooftops.jpg" "Coastline Journal/douro-valley.jpg" "Coastline Journal/images/")
for t in cutsheet winpid sheet; do swiftc -O "$HERE/$t.swift" -o "$S/l10n/$t"; done
for l in en de fr es it pt nl ja zh; do python3 "$S/l10n/demo.py" $l "$S/l10n/$l"; done
echo "ready in $S"
