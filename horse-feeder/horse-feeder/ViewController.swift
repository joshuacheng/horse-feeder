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
import Alamofire
//import SpeechToTextV1

import Firebase
import SwiftyJSON

class ViewController: UIViewController, AVCapturePhotoCaptureDelegate {
    var captureSesssion : AVCaptureSession!
    var cameraOutput : AVCapturePhotoOutput!
    var previewLayer : AVCaptureVideoPreviewLayer!
    var ngrok = "https://f05fa865.ngrok.io"
    
    @IBOutlet var previewView: UIView!
    
    @IBOutlet var capturedImage: UIImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        captureSesssion = AVCaptureSession()
        captureSesssion.sessionPreset = AVCaptureSession.Preset.photo
        cameraOutput = AVCapturePhotoOutput()
        
        let device = AVCaptureDevice.default(for: .video)
        
        if let input = try? AVCaptureDeviceInput(device: device!) {
            if (captureSesssion.canAddInput(input)) {
                captureSesssion.addInput(input)
                if (captureSesssion.canAddOutput(cameraOutput)) {
                    captureSesssion.addOutput(cameraOutput)
                    previewLayer = AVCaptureVideoPreviewLayer(session: captureSesssion)
                    previewLayer.frame = previewView.bounds
                    previewView.layer.addSublayer(previewLayer)
                    captureSesssion.startRunning()
                }
            } else {
                print("issue here : captureSesssion.canAddInput")
            }
        } else {
            print("some problem here")
        }
    }
    var timer = Timer()
    
    @IBAction func takePhoto(_ sender: Any) {
        timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.take_pic), userInfo: nil, repeats: true)
    }
    
    @objc func take_pic() {
        let settings = AVCapturePhotoSettings()
        let previewPixelType = settings.availablePreviewPhotoPixelFormatTypes.first!
        let previewFormat = [
            kCVPixelBufferPixelFormatTypeKey as String: previewPixelType,
            kCVPixelBufferWidthKey as String: 160,
            kCVPixelBufferHeightKey as String: 160
        ]
        settings.previewPhotoFormat = previewFormat
        cameraOutput.capturePhoto(with: settings, delegate: self as! AVCapturePhotoCaptureDelegate)
    }
    
    
    // callBack from take picture
    func photoOutput(_ captureOutput: AVCapturePhotoOutput, didFinishProcessingPhoto photoSampleBuffer: CMSampleBuffer?, previewPhoto previewPhotoSampleBuffer: CMSampleBuffer?, resolvedSettings: AVCaptureResolvedPhotoSettings, bracketSettings: AVCaptureBracketedStillImageSettings?, error: Error?) {
        
        if let error = error {
            print("error occure : \(error.localizedDescription)")
        }
        
        if  let sampleBuffer = photoSampleBuffer,
            let previewBuffer = previewPhotoSampleBuffer,
            let dataImage =  AVCapturePhotoOutput.jpegPhotoDataRepresentation(forJPEGSampleBuffer:  sampleBuffer, previewPhotoSampleBuffer: previewBuffer) {
            print(UIImage(data: dataImage)?.size as Any)
            
            let dataProvider = CGDataProvider(data: dataImage as CFData)
            let cgImageRef: CGImage! = CGImage(jpegDataProviderSource: dataProvider!, decode: nil, shouldInterpolate: true, intent: .defaultIntent)
            let image = UIImage(cgImage: cgImageRef, scale: 1.0, orientation: UIImageOrientation.right)
            
                self.capturedImage.image = image
            //            var json = {
            //                    "requests": [
            //                    {
            //                    "image":{
            //                    "content":"/9j/7QBEUGhvdG9...image contents...eYxxxzj/Coa6Bax//Z"
            //                    },
            //                    "features":[
            //                    {
            //                    "type":"LABEL_DETECTION",
            //                    "maxResults":1
            //                    }
            //                    ]
            //                    }
            //                    ]
            //            }
            var image2 = UIImage(named: "lol")
            capturedImage.image = image2
            let imageData: Data? = UIImageJPEGRepresentation(image2!, 0.4)
            let imageStr = imageData?.base64EncodedString(options: .lineLength64Characters)
            let parameters = [
                "requests": [
                    "image": [
                        "content": imageStr
                    ],
                    "features": [
                        [
                            "type": "LABEL_DETECTION",
                            "maxResults": 10
                        ],
                        [
                            "type": "FACE_DETECTION",
                            "maxResults": 10
                        ]
                    ]
                ]
            ]
            
            //            print("hello")
            //                Alamofire.request("https://vision.googleapis.com/v1/images:annotate?key=AIzaSyBi6k04pmZZNw5FWf0uqFHY1skme0-_FtE", method: .post, parameters: parameters, encoding: JSONEncoding.default)
            //                    .responseJSON { response in
            //                        print(response)
            //                        print("did this even work")
            //                }
            // here
            createRequest(with: imageStr!)
            
        }
        
        else {
            print("some error here")
        }
    }
    func createRequest(with imageBase64: String) {
        // Create our request URL
        
        var googleAPIKey = "AIzaSyBi6k04pmZZNw5FWf0uqFHY1skme0-_FtE"
        var googleURL: URL {
            return URL(string: "https://vision.googleapis.com/v1/images:annotate?key=\(googleAPIKey)")!
        }
        var request = URLRequest(url: googleURL)
        
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue(Bundle.main.bundleIdentifier ?? "", forHTTPHeaderField: "X-Ios-Bundle-Identifier")
        
        // Build our API request
        let jsonRequest = [
            "requests": [
                "image": [
                    "content": imageBase64
                ],
                "features": [
                    [
//                        "type": "TEXT_DETECTION",
//                        "maxResults": 10
//                    ],
//                    [
                        "type": "TEXT_DETECTION",
                        "maxResults": 1
                    ]
                ]
            ]
        ]
        let jsonObject = JSON(jsonRequest)
        
        // Serialize the JSON
        guard let data = try? jsonObject.rawData() else {
            return
        }
        
        request.httpBody = data
        
        // Run the request on a background thread
        DispatchQueue.global().async { self.runRequestOnBackgroundThread(request) }
    }
    let session = URLSession.shared
    func runRequestOnBackgroundThread(_ request: URLRequest) {
        // run the request
        //        print("hello1")
        let task: URLSessionDataTask = session.dataTask(with: request) { (data, response, error) in
            guard let data = data, error == nil else {
                print(error?.localizedDescription ?? "")
                print("hello2")
                return
            }
            print("---------------------")
//            let responseJSON = try? JSONSerialization.jsonObject(with: data, options: [])
//            if let responseJSON = responseJSON as? [String: Any] {
                let json = try! JSON(data: data)
                let errorObj: JSON = json["error"]
                    let responses: JSON = json["responses"][0]
            let name = responses["fullTextAnnotation"]["text"] as? String

                    print(responses["fullTextAnnotation"]["text"]) // HERE IT FRICKIN ISSSSSS GODNBLESLEKJSKLT
            Alamofire.request("\(self.ngrok)/horse?horse=\(responses["fullTextAnnotation"]["text"].string!.dropLast(2))").response { response in
                        print(response)
                    }
            
            }
            
        
        
        task.resume()
    }
    
    // This method you can use somewhere you need to know camera permission   state
    func askPermission() {
        print("here")
        let cameraPermissionStatus =  AVCaptureDevice.authorizationStatus(for: AVMediaType.video)
        
        switch cameraPermissionStatus {
        case .authorized:
            print("Already Authorized")
        case .denied:
            print("denied")
            
            let alert = UIAlertController(title: "Sorry :(" , message: "But  could you please grant permission for camera within device settings",  preferredStyle: .alert)
            let action = UIAlertAction(title: "Ok", style: .cancel,  handler: nil)
            alert.addAction(action)
            present(alert, animated: true, completion: nil)
            
        case .restricted:
            print("restricted")
        default:
            AVCaptureDevice.requestAccess(for: AVMediaType.video, completionHandler: {
                [weak self]
                (granted :Bool) -> Void in
                
                if granted == true {
                    // User granted
                    print("User granted")
                    DispatchQueue.main.async(){
                        //Do smth that you need in main thread
                    }
                }
                else {
                    // User Rejected
                    print("User Rejected")
                    
                    DispatchQueue.main.async(){
                        let alert = UIAlertController(title: "WHY?" , message:  "Camera it is the main feature of our application", preferredStyle: .alert)
                        let action = UIAlertAction(title: "Ok", style: .cancel, handler: nil)
                        alert.addAction(action)
                        self?.present(alert, animated: true, completion: nil)
                    }
                }
            });
        }
    }
}

