// Cuts the main object out of a still frame as a transparent PNG, cropped to the object.
//
// Usage: object_cutout <frame.png> <out.png> <x,y,w,h>
// Extract the frame with ffmpeg first (it applies the take's rotation):
//   ffmpeg -ss 3.2 -i tomas/<Reel>/8_b_bloque_yoga.mp4 -frames:v 1 frame.png
// x,y,w,h is a box around the object, in fractions of the frame from the top left:
// over the whole frame Vision only sees the person, but inside the box the object is
// the foreground. Apple Vision finds the foreground instances (macOS 14+); instances
// that are mostly the person are dropped and the person mask is subtracted from the
// rest, so a hand holding the object is not kept. The largest remaining one is kept.

import CoreImage
import Foundation
import ImageIO
import Vision

func fail(_ message: String) -> Never {
    FileHandle.standardError.write("object_cutout: \(message)\n".data(using: .utf8)!)
    exit(1)
}

let args = CommandLine.arguments
guard args.count == 4 else {
    FileHandle.standardError.write("usage: object_cutout <frame.png> <out.png> <x,y,w,h>\n".data(using: .utf8)!)
    exit(2)
}
let box = args[3].split(separator: ",").compactMap { Double($0) }
guard box.count == 4 else { fail("the box must be x,y,w,h") }

guard let source = CGImageSourceCreateWithURL(URL(fileURLWithPath: args[1]) as CFURL, nil),
      let frame = CGImageSourceCreateImageAtIndex(source, 0, nil),
      let image = frame.cropping(to: CGRect(
          x: box[0] * Double(frame.width), y: box[1] * Double(frame.height),
          width: box[2] * Double(frame.width), height: box[3] * Double(frame.height)
      ))
else { fail("cannot read \(args[1])") }
let width = image.width, height = image.height

let handler = VNImageRequestHandler(cgImage: image)
let instancesRequest = VNGenerateForegroundInstanceMaskRequest()
let personRequest = VNGeneratePersonSegmentationRequest()
personRequest.qualityLevel = .accurate
personRequest.outputPixelFormat = kCVPixelFormatType_OneComponent8
do {
    try handler.perform([instancesRequest, personRequest])
} catch {
    fail("vision failed: \(error)")
}
guard let instances = instancesRequest.results?.first else { fail("no foreground object found") }

// Person mask at full resolution, 0...1.
let context = CIContext(options: [.workingColorSpace: NSNull()])
var person = [UInt8](repeating: 0, count: width * height)
if let mask = personRequest.results?.first?.pixelBuffer {
    let small = CIImage(cvPixelBuffer: mask)
    let scaled = small.transformed(by: CGAffineTransform(
        scaleX: CGFloat(width) / small.extent.width, y: CGFloat(height) / small.extent.height
    ))
    context.render(scaled, toBitmap: &person, rowBytes: width,
                   bounds: CGRect(x: 0, y: 0, width: width, height: height), format: .L8, colorSpace: nil)
}

func instanceMask(_ index: Int) -> [Float] {
    guard let buffer = try? instances.generateScaledMaskForImage(forInstances: [index], from: handler) else {
        fail("cannot build mask for instance \(index)")
    }
    CVPixelBufferLockBaseAddress(buffer, .readOnly)
    defer { CVPixelBufferUnlockBaseAddress(buffer, .readOnly) }
    let rowFloats = CVPixelBufferGetBytesPerRow(buffer) / MemoryLayout<Float>.size
    let base = CVPixelBufferGetBaseAddress(buffer)!.assumingMemoryBound(to: Float.self)
    var mask = [Float](repeating: 0, count: width * height)
    for y in 0..<height {
        for x in 0..<width {
            mask[y * width + x] = base[y * rowFloats + x]
        }
    }
    return mask
}

// Keep the largest instance that is not mostly the person.
var best: (mask: [Float], area: Double)?
for index in instances.allInstances {
    let mask = instanceMask(index)
    var area = 0.0, personArea = 0.0
    for i in 0..<mask.count where mask[i] > 0.5 {
        area += 1
        if person[i] > 127 { personArea += 1 }
    }
    if area == 0 || personArea / area > 0.5 { continue }
    if best == nil || area > best!.area { best = (mask, area) }
}
guard let object = best?.mask else { fail("only the person was found") }

// Straight-alpha RGBA, cropped to the object.
var pixels = [UInt8](repeating: 0, count: width * height * 4)
let rgb = CGColorSpace(name: CGColorSpace.sRGB)!
let drawing = CGContext(data: &pixels, width: width, height: height, bitsPerComponent: 8, bytesPerRow: width * 4,
                        space: rgb, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
drawing.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))

var minX = width, minY = height, maxX = -1, maxY = -1
for y in 0..<height {
    for x in 0..<width {
        let i = y * width + x
        let alpha = object[i] * (1 - Float(person[i]) / 255)
        pixels[i * 4 + 3] = UInt8(max(0, min(255, alpha * 255)))
        if alpha > 0.1 {
            minX = min(minX, x); maxX = max(maxX, x); minY = min(minY, y); maxY = max(maxY, y)
        }
    }
}
guard maxX >= 0 else { fail("the object is hidden by the person") }
if minX == 0 || minY == 0 || maxX == width - 1 || maxY == height - 1 {
    FileHandle.standardError.write("object_cutout: warning, the object touches the box edge and may be cut\n".data(using: .utf8)!)
}

let provider = CGDataProvider(data: Data(pixels) as CFData)!
let full = CGImage(width: width, height: height, bitsPerComponent: 8, bitsPerPixel: 32, bytesPerRow: width * 4,
                   space: rgb, bitmapInfo: CGBitmapInfo(rawValue: CGImageAlphaInfo.last.rawValue),
                   provider: provider, decode: nil, shouldInterpolate: false, intent: .defaultIntent)!
let cropped = full.cropping(to: CGRect(x: minX, y: minY, width: maxX - minX + 1, height: maxY - minY + 1))!
guard let destination = CGImageDestinationCreateWithURL(URL(fileURLWithPath: args[2]) as CFURL, "public.png" as CFString, 1, nil)
else { fail("cannot write \(args[2])") }
CGImageDestinationAddImage(destination, cropped, nil)
guard CGImageDestinationFinalize(destination) else { fail("cannot write \(args[2])") }
print("\(args[2]): \(cropped.width)x\(cropped.height)")
