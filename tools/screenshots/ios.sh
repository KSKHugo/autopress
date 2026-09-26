#!/bin/zsh
# ios.sh <lang> <step>
#   prep     boot both simulators in that language, install the demo, start the mock
#   detail   iPhone: open the Lisbon post, screenshot (to find the Crop button)
#   crop     screenshot after the crop editor was opened by a tap
#   rest     iPhone schedule + list, iPad upload run
#   done     restore German, shut down, stop the mock
L=$1; STEP=$2
S="${AUTOPRESS_SHOTS:-$HOME/Library/Caches/AutoPress-Shots}"   # work folder, see setup.sh
IPAD=EDD5C2DA-BEDA-42EE-8341-E27EF58AC470; IPHONE=A44CB2DC-7F00-441A-8E75-BB325226CB25
SIMAPP="$HOME/Library/Caches/AutoPress-DerivedData/Build/Products/Debug-iphonesimulator/Hybrid AutoPress.app"
OUT="$S/shots/$L"; mkdir -p "$OUT"
typeset -A LANGS LOCALES
LANGS=(en en-US de de-DE fr fr-FR es es-ES it it-IT pt pt-PT nl nl-NL ja ja-JP zh zh-Hans-CN)
LOCALES=(en en_US de de_DE fr fr_FR es es_ES it it_IT pt pt_PT nl nl_NL ja ja_JP zh zh_CN)
launch() { local d=$1; shift; local C=$(xcrun simctl get_app_container $d de.pascalhugo.autopress data)
  xcrun simctl terminate $d de.pascalhugo.autopress 2>/dev/null; sleep 1
  xcrun simctl launch $d de.pascalhugo.autopress -demoFolder "$C/Documents/Coastline Journal" -demoSite http://localhost:8881 -demoUser tester -demoPassword "abcd EFGH 1234 ijkl" "$@" >/dev/null; }
shot() { xcrun simctl io $1 screenshot "$OUT/$2.png" 2>/dev/null; }
case $STEP in
prep)
  pkill -f "mock.py 8881"; sleep 0.5
  (cd "$S/demo" && python3 mock.py 8881 "$S/demo/requests.json" "$S/l10n/$L/terms.json" >/dev/null 2>&1 &)
  for d in $IPAD $IPHONE; do
    xcrun simctl boot $d 2>/dev/null; xcrun simctl bootstatus $d -b >/dev/null
    xcrun simctl spawn $d defaults write "Apple Global Domain" AppleLanguages -array ${LANGS[$L]}
    xcrun simctl spawn $d defaults write "Apple Global Domain" AppleLocale -string ${LOCALES[$L]}
    xcrun simctl shutdown $d; xcrun simctl boot $d; xcrun simctl bootstatus $d -b >/dev/null
    xcrun simctl status_bar $d override --time "9:41" --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3
    xcrun simctl install $d "$SIMAPP"
    C=$(xcrun simctl get_app_container $d de.pascalhugo.autopress data); mkdir -p "$C/Documents"
    rm -rf "$C/Documents/Coastline Journal"; cp -R "$S/l10n/$L/Coastline Journal" "$C/Documents/"
  done ;;
detail)
  launch $IPHONE -demoSelect 2; sleep 17; shot $IPHONE iphone-detail
  sips -Z 900 "$OUT/iphone-detail.png" --out "$OUT/p-iphone-detail.png" >/dev/null ;;
crop)
  sleep 2; shot $IPHONE iphone-crop; sips -Z 900 "$OUT/iphone-crop.png" --out "$OUT/p-iphone-crop.png" >/dev/null ;;
rest)
  launch $IPAD -demoSelect 2 -demoUpload YES
  launch $IPHONE; sleep 15; shot $IPHONE iphone-list
  sleep 12; shot $IPAD ipad-done
  launch $IPHONE -demoSelect 2; sleep 17
  echo ready-for-schedule-tap ;;
schedule)
  sleep 1.5; shot $IPHONE iphone-schedule
  for f in iphone-list iphone-schedule ipad-done; do sips -Z 900 "$OUT/$f.png" --out "$OUT/p-$f.png" >/dev/null; done ;;
done)
  for d in $IPAD $IPHONE; do xcrun simctl status_bar $d clear
    xcrun simctl spawn $d defaults write "Apple Global Domain" AppleLanguages -array de-DE
    xcrun simctl spawn $d defaults write "Apple Global Domain" AppleLocale -string de_DE
    xcrun simctl shutdown $d; done
  pkill -f "mock.py 8881" ;;
esac
