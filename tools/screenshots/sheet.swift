// sheet <out.png> <cols> <cell width> <files…>: a contact sheet
import AppKit
let a = CommandLine.arguments; let cols = Int(a[2])!, cw = CGFloat(Int(a[3])!)
let imgs = a.dropFirst(4).map { NSImage(contentsOfFile: $0)! }
let ch = imgs.map { cw * $0.size.height / $0.size.width }.max()!
let rows = (imgs.count + cols - 1) / cols
let out = NSImage(size: NSSize(width: cw * CGFloat(cols), height: ch * CGFloat(rows)))
out.lockFocus(); NSColor.white.setFill(); NSRect(origin: .zero, size: out.size).fill()
for (i, im) in imgs.enumerated() {
  let h = cw * im.size.height / im.size.width
  im.draw(in: NSRect(x: CGFloat(i % cols) * cw, y: out.size.height - CGFloat(i / cols + 1) * ch + (ch - h), width: cw, height: h))
}
out.unlockFocus()
let rep = NSBitmapImageRep(data: out.tiffRepresentation!)!
try! rep.representation(using: .jpeg, properties: [.compressionFactor: 0.8])!.write(to: URL(fileURLWithPath: a[1]))
