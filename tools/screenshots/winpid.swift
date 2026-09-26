// winpid <pid>: on-screen windows of that process: id and bounds
import CoreGraphics
import Foundation
let pid = Int(CommandLine.arguments[1])!
let list = CGWindowListCopyWindowInfo([.optionOnScreenOnly], kCGNullWindowID) as! [[String: Any]]
for w in list where (w["kCGWindowOwnerPID"] as? Int) == pid && (w["kCGWindowLayer"] as? Int) == 0 {
  print(w["kCGWindowNumber"] as! Int, (w["kCGWindowBounds"] as! [String: Any]).description.replacingOccurrences(of: "\n", with: " "))
}
