// cutsheet <window.png> <out.png>: cuts the Pro sheet out of a window capture by
// finding its navy header (the dimmed window behind it is grey, never navy).
import AppKit
let args = CommandLine.arguments
let rep = NSBitmapImageRep(data: try! Data(contentsOf: URL(fileURLWithPath: args[1])))!
let w = rep.pixelsWide, h = rep.pixelsHigh
func navy(_ x: Int, _ y: Int) -> Bool {
    guard let c = rep.colorAt(x: x, y: y)?.usingColorSpace(.sRGB) else { return false }
    return c.blueComponent > 0.28 && c.blueComponent < 0.55 && c.redComponent < 0.22 && c.blueComponent - c.redComponent > 0.15
}
// the header row: the first row from the top with a long navy run
var top = 0, left = 0, right = 0
outer: for y in stride(from: 0, to: h / 2, by: 2) {
    var run = 0, start = 0
    for x in 0..<w {
        if navy(x, y) { if run == 0 { start = x }; run += 1 } else {
            if run > w / 4 { top = y; left = start; right = x; break outer }
            run = 0
        }
    }
}
// widen to the sheet's rounded top corners: step down a few rows and take the widest run
var l = left, r = right
for y in top..<min(top + 60, h) {
    var x = left; while x > 0 && navy(x - 1, y) { x -= 1 }; l = min(l, x)
    x = right; while x < w - 1 && navy(x, y) { x += 1 }; r = max(r, x)
}
let rect = NSRect(x: l, y: top, width: r - l, height: h - top - 24)
let cg = rep.cgImage!.cropping(to: rect)!
try! NSBitmapImageRep(cgImage: cg).representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[2]))
print("sheet", l, top, r - l, h - top - 24)
