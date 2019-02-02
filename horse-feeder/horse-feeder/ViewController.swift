//
//  ViewController.swift
//  horse-feeder
//
//  Created by Emily on 2/1/19.
//  Copyright © 2019 Emily. All rights reserved.
//

import UIKit
import Foundation
import AVFoundation
import Photos
//import Alamofire
//import SpeechToTextV1

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate, AVAudioPlayerDelegate, AVAudioRecorderDelegate {
    
    var session: AVCaptureSession!
    var input: AVCaptureDeviceInput!
    var output: AVCaptureStillImageOutput!
    var previewLayer: AVCaptureVideoPreviewLayer!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func capture(_ sender: Any) {
        self.setupSession()
        capturePhoto()
    }
    func setupSession() {
        print("haaaeaea")
//        print(ngrok)
        session = AVCaptureSession()
        session.sessionPreset = AVCaptureSession.Preset.photo
        
        let camera = AVCaptureDevice.default(for: .video)

        
        do { input = try AVCaptureDeviceInput(device: camera!) } catch { return }
        
        output = AVCaptureStillImageOutput()
        output.outputSettings = [ AVVideoCodecKey: AVVideoCodecType.jpeg ]
        
        guard session.canAddInput(input)
            && session.canAddOutput(output) else { return }
        
        session.addInput(input)
        session.addOutput(output)
        
        previewLayer = AVCaptureVideoPreviewLayer(session: session)
        
        previewLayer!.videoGravity = AVLayerVideoGravity.resizeAspect
        previewLayer!.connection?.videoOrientation = .portrait
        
        view.layer.addSublayer(previewLayer!)
        
        session.startRunning()
    }
    func timerCalled(timer: Timer) {
        capturePhoto()
        print("HEYYYYYYYYYYYYYY")
    }
    func capturePhoto() {
        guard let connection = output.connection(with: AVMediaType.video) else { return }
        connection.videoOrientation = .portrait
        
        output.captureStillImageAsynchronously(from: connection) { (sampleBuffer, error) in
            guard sampleBuffer != nil && error == nil else { return }
            let imageData = AVCaptureStillImageOutput.jpegStillImageNSDataRepresentation(sampleBuffer!)
            guard let image = UIImage(data: imageData!) else { return }
            let imageJPG: Data! = UIImageJPEGRepresentation(image, 0.1)
//            Alamofire.request("\(self.ngrok)\((imageJPG as NSData).base64EncodedString(options: NSData.Base64EncodingOptions(rawValue: 0)))")
//            print("\(self.ngrok)\((imageJPG as NSData).base64EncodedString(options: NSData.Base64EncodingOptions(rawValue: 0)))")
        }
    }

}

