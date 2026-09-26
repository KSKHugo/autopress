#!/bin/zsh
# mac.sh <lang>: the six Mac screenshots for the website, in that language
L=$1
S="${AUTOPRESS_SHOTS:-$HOME/Library/Caches/AutoPress-Shots}"   # work folder, see setup.sh
D="$HOME/Library/Containers/de.pascalhugo.autopress/Data/Documents"
APP="$HOME/Library/Caches/AutoPress-DerivedData/Build/Products/Debug/Hybrid AutoPress.app"
OUT="$S/shots/$L"; mkdir -p "$OUT"
typeset -A LANGS LOCALES
LANGS=(en en de de fr fr es es it it pt pt-PT nl nl ja ja zh zh-Hans)
LOCALES=(en en_US de de_DE fr fr_FR es es_ES it it_IT pt pt_PT nl nl_NL ja ja_JP zh zh_Hans_CN)
pkill -f "mock.py 8881"; sleep 1
MYAPP="AutoPress-DerivedData/Build/Products/Debug/Hybrid AutoPress.app/Contents/MacOS"
stop() { pkill -f "$MYAPP"; }
(cd "$S/demo" && python3 mock.py 8881 "$S/demo/requests.json" "$S/l10n/$L/terms.json" >/dev/null 2>&1 &)
rm -rf "$D/Coastline Journal"; mkdir -p "$D"; cp -R "$S/l10n/$L/Coastline Journal" "$D/"
sleep 1
start() { stop; sleep 1.5
  open -n -a "$APP" --args -AppleLanguages "(${LANGS[$L]})" -AppleLocale ${LOCALES[$L]} -demoFolder "$D/Coastline Journal" -demoSelect 2 -demoSite http://localhost:8881 -demoUser tester -demoPassword "abcd EFGH 1234 ijkl" "$@"; sleep 1; PID=$(pgrep -n -f "$MYAPP"); }
launch() { start "$@"; sleep 8; }
wins() { "$S/l10n/winpid" $PID; }
main_id() { wins | grep '"Width": 1040' | awk '{print $1}' | head -1; }
cap() { screencapture -x -l $(main_id) "$OUT/$1.png"; }
region() { local b=$(wins | grep '"Width": 1040' | head -1)
  local x=$(echo $b | sed 's/.*"X": \([0-9]*\).*/\1/') y=$(echo $b | sed 's/.*"Y": \([0-9]*\).*/\1/')
  screencapture -x -R "$x,$y,1040,700" "$OUT/$1.png"; }
ui() { osascript -e "tell application \"System Events\" to tell (first process whose unix id is $PID)" -e 'set frontmost to true' -e "$1" -e 'end tell' >/dev/null; }
SIDE='outline 1 of scroll area 1 of group 1 of splitter group 1 of group 1 of window 1'

want() { [ -z "$ONLY" ] || [[ " $ONLY " == *" $1 "* ]]; }
if want main || want schedule; then
launch; cap mac-main
ui "click pop up button 1 of UI element 1 of row 5 of $SIDE"; sleep 0.7
ui "click menu item 3 of menu 1 of pop up button 1 of UI element 1 of row 5 of $SIDE"; sleep 1.5
ui "click pop up button 1 of UI element 1 of row 7 of $SIDE"; sleep 0.7
ui "click menu item 4 of menu 1 of pop up button 1 of UI element 1 of row 7 of $SIDE"; sleep 1.5
cap mac-schedule
fi
if want categories || want pro; then

launch
ui 'click button 1 of group 4 of scroll area 1 of group 2 of splitter group 1 of group 1 of window 1'; sleep 3
region mac-categories
ui 'key code 53'; sleep 1
ui 'click menu bar item 2 of menu bar 1'; sleep 0.6
ui 'click (first menu item of menu 1 of menu bar item 2 of menu bar 1 whose name starts with "AutoPress Pro")'; sleep 3
wins > "$OUT/pro-windows.txt"
sheet=$(grep -v '"Width": 1040' "$OUT/pro-windows.txt" | awk '{print $1}' | head -1)
# The sheet is composited into its parent: capture the window without shadow and cut
# the sheet out by the bounds the window server reports (points × 2).
screencapture -x -o -l $(main_id) "$OUT/mac-pro-window.png"
python3 - "$OUT/pro-windows.txt" "$OUT/mac-pro-window.png" "$OUT/mac-pro.png" <<'PY'
import re, subprocess, sys
rows = [dict(re.findall(r'"(\w+)": (\d+)', l)) for l in open(sys.argv[1])]
main = next(r for r in rows if r["Width"] == "1040"); sheet = next(r for r in rows if r["Width"] != "1040")
x = (int(sheet["X"]) - int(main["X"])) * 2; y = (int(sheet["Y"]) - int(main["Y"])) * 2
w = int(sheet["Width"]) * 2; h = min(int(sheet["Height"]) * 2, 1400 - y) - 8
subprocess.run(["sips", "--cropToHeightWidth", str(h), str(w), "--cropOffset", str(y), str(x), sys.argv[2], "--out", sys.argv[3]], capture_output=True)
PY
ui 'key code 53'
fi
if want done || want uploading; then
start -demoUpload YES
sleep 5; cap mac-uploading
sleep 16; cap mac-done
fi
stop; pkill -f "mock.py 8881"
rm -rf "$D/Coastline Journal"
ls "$OUT"
