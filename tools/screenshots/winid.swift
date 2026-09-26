import CoreGraphics
import Foundation
let list = CGWindowListCopyWindowInfo([.optionOnScreenOnly], kCGNullWindowID) as! [[String: Any]]
for w in list where (w["kCGWindowOwnerName"] as? String ?? "").contains("AutoPress") && (w["kCGWindowLayer"] as? Int) == 0 {
  print(w["kCGWindowNumber"] as! Int, (w["kCGWindowBounds"] as! [String: Any]).description.replacingOccurrences(of: "\n", with: " "))
}
