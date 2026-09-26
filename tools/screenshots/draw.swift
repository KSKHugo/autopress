import AppKit
struct Scene { let name: String; let sky: [(CGFloat,CGFloat,CGFloat)]; let hills: [(CGFloat,CGFloat,CGFloat)]; let sun: CGPoint; let seed: UInt64 }
let scenes = [
 Scene(name:"lisbon-in-three-days", sky:[(0.99,0.78,0.52),(0.96,0.55,0.40)], hills:[(0.78,0.42,0.36),(0.52,0.27,0.33),(0.26,0.17,0.30)], sun:CGPoint(x:0.72,y:0.62), seed:3),
 Scene(name:"porto-by-tram", sky:[(0.62,0.80,0.93),(0.90,0.93,0.92)], hills:[(0.45,0.62,0.70),(0.24,0.43,0.55),(0.10,0.23,0.37)], sun:CGPoint(x:0.25,y:0.75), seed:7),
 Scene(name:"algarve-cliffs", sky:[(0.40,0.72,0.90),(0.80,0.92,0.95)], hills:[(0.93,0.74,0.45),(0.85,0.58,0.30),(0.15,0.45,0.60)], sun:CGPoint(x:0.55,y:0.80), seed:11),
 Scene(name:"alfama-rooftops", sky:[(0.98,0.85,0.70),(0.95,0.68,0.55)], hills:[(0.85,0.50,0.35),(0.65,0.33,0.28),(0.35,0.18,0.22)], sun:CGPoint(x:0.40,y:0.55), seed:17),
 Scene(name:"douro-valley", sky:[(0.70,0.85,0.80),(0.95,0.95,0.85)], hills:[(0.55,0.70,0.45),(0.33,0.52,0.33),(0.15,0.32,0.25)], sun:CGPoint(x:0.80,y:0.70), seed:23),
 Scene(name:"sintra-palace", sky:[(0.80,0.78,0.92),(0.98,0.90,0.86)], hills:[(0.60,0.55,0.70),(0.40,0.35,0.55),(0.22,0.18,0.35)], sun:CGPoint(x:0.30,y:0.66), seed:29),
 Scene(name:"packing-list", sky:[(0.95,0.93,0.88),(0.99,0.97,0.94)], hills:[(0.80,0.70,0.55),(0.60,0.50,0.40),(0.35,0.30,0.28)], sun:CGPoint(x:0.60,y:0.72), seed:31),
]
let W = 2400, H = 1500
for s in scenes {
  var state = s.seed
  func rnd() -> CGFloat { state = state &* 6364136223846793005 &+ 1442695040888963407; return CGFloat((state >> 33) % 1000) / 1000 }
  let rep = NSBitmapImageRep(bitmapDataPlanes:nil, pixelsWide:W, pixelsHigh:H, bitsPerSample:8, samplesPerPixel:4, hasAlpha:true, isPlanar:false, colorSpaceName:.deviceRGB, bytesPerRow:0, bitsPerPixel:0)!
  let ctx = NSGraphicsContext(bitmapImageRep: rep)!.cgContext
  let cs = CGColorSpace(name: CGColorSpace.sRGB)!
  let sky = CGGradient(colorsSpace: cs, colors: s.sky.map{ CGColor(srgbRed:$0.0,green:$0.1,blue:$0.2,alpha:1) } as CFArray, locations:[0,1])!
  ctx.drawLinearGradient(sky, start: CGPoint(x:0,y:H), end: CGPoint(x:0,y:Int(Double(H)*0.3)), options: [.drawsAfterEndLocation])
  let sc = CGPoint(x: s.sun.x*CGFloat(W), y: s.sun.y*CGFloat(H))
  let glow = CGGradient(colorsSpace: cs, colors:[CGColor(srgbRed:1,green:0.97,blue:0.85,alpha:0.95),CGColor(srgbRed:1,green:0.95,blue:0.8,alpha:0)] as CFArray, locations:[0,1])!
  ctx.drawRadialGradient(glow, startCenter: sc, startRadius: 60, endCenter: sc, endRadius: 540, options: [])
  ctx.setFillColor(CGColor(srgbRed:1,green:0.98,blue:0.9,alpha:1)); ctx.fillEllipse(in: CGRect(x: sc.x-90,y: sc.y-90,width:180,height:180))
  for (i,h) in s.hills.enumerated() {
    let base = CGFloat(H)*(0.52 - CGFloat(i)*0.15)
    let amp = CGFloat(135 - i*22); let f1 = 1.5+rnd()*2, f2 = 4+rnd()*3, p1 = rnd()*6, p2 = rnd()*6
    let path = CGMutablePath(); path.move(to: CGPoint(x:0,y:0))
    for x in stride(from: 0, through: W, by: 8) {
      let t = CGFloat(x)/CGFloat(W)
      path.addLine(to: CGPoint(x: CGFloat(x), y: base + amp*sin(t*f1*3.14+p1) + amp*0.35*sin(t*f2*3.14+p2)))
    }
    path.addLine(to: CGPoint(x:W,y:0)); path.closeSubpath()
    ctx.addPath(path); ctx.setFillColor(CGColor(srgbRed:h.0,green:h.1,blue:h.2,alpha:1)); ctx.fillPath()
  }
  let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.88])!
  try! data.write(to: URL(fileURLWithPath: "Coastline Journal/\(s.name).jpg"))
}
