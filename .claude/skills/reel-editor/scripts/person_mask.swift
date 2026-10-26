// Streams a per-frame person mask of a video as raw 8-bit gray frames on stdout.
//
// Usage: person_mask <video> <width> <height>
// Frames come out at the video's native frame rate, scaled to width x height, so
// ffmpeg can read them with `-f rawvideo -pix_fmt gray -s WxH`. The video must not
// carry a rotation transform (run it on the cut, which ffmpeg already rotated).

import AVFoundation
import CoreImage
import Foundation
import Vision

let args = CommandLine.arguments
guard args.count == 4, let width = Int(args[2]), let height = Int(args[3]) else {
    FileHandle.standardError.write("usage: person_mask <video> <width> <height>\n".data(using: .utf8)!)
    exit(2)
}

func fail(_ message: String) -> Never {
    FileHandle.standardError.write("person_mask: \(message)\n".data(using: .utf8)!)
    exit(1)
}

let asset = AVURLAsset(url: URL(fileURLWithPath: args[1]))
let semaphore = DispatchSemaphore(value: 0)
var loadedTrack: AVAssetTrack?
Task {
    loadedTrack = try? await asset.loadTracks(withMediaType: .video).first
    semaphore.signal()
}
semaphore.wait()
guard let track = loadedTrack else { fail("no video track") }

guard let reader = try? AVAssetReader(asset: asset) else { fail("cannot open reader") }
let output = AVAssetReaderTrackOutput(
    track: track,
    outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA]
)
output.alwaysCopiesSampleData = false
reader.add(output)
reader.startReading()

// The sequence handler carries state between frames, which steadies the mask edges.
let sequenceHandler = VNSequenceRequestHandler()
let request = VNGeneratePersonSegmentationRequest()
request.qualityLevel = .accurate
request.outputPixelFormat = kCVPixelFormatType_OneComponent8

let context = CIContext(options: [.workingColorSpace: NSNull()])
let frameBytes = width * height
var gray = [UInt8](repeating: 0, count: frameBytes)
let stdout = FileHandle.standardOutput

while let sample = output.copyNextSampleBuffer() {
    guard let frame = CMSampleBufferGetImageBuffer(sample) else { continue }
    do {
        try sequenceHandler.perform([request], on: frame)
    } catch {
        fail("segmentation failed: \(error)")
    }
    if let mask = request.results?.first?.pixelBuffer {
        let image = CIImage(cvPixelBuffer: mask)
        let scaled = image.transformed(by: CGAffineTransform(
            scaleX: CGFloat(width) / image.extent.width,
            y: CGFloat(height) / image.extent.height
        ))
        context.render(
            scaled, toBitmap: &gray, rowBytes: width,
            bounds: CGRect(x: 0, y: 0, width: width, height: height),
            format: .L8, colorSpace: nil
        )
    } else {
        gray.withUnsafeMutableBufferPointer { $0.update(repeating: 0) }
    }
    stdout.write(Data(gray))
}

if reader.status == .failed {
    fail("reader failed: \(reader.error?.localizedDescription ?? "unknown")")
}
