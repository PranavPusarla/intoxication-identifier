//
//  ViewController.swift
//  IntoxicationIdentifier
//
//  Created by Chandrasekhar pusarla on 8/7/20.
//  Copyright © 2020 Pranav Pusarla. All rights reserved.
//

import UIKit
import AVFoundation
class ViewController: UIViewController, UIImagePickerControllerDelegate & UINavigationControllerDelegate {

    @IBOutlet weak var littleImage: UIImageView!
    @IBOutlet weak var photo: UIImageView!
    @IBOutlet weak var button: UIButton!
    var imagePicker: UIImagePickerController!
    var captureSession = AVCaptureSession()
    var backCamera: AVCaptureDevice?
    var frontCamera: AVCaptureDevice?
    var currentCamera: AVCaptureDevice?
    var photoOutput: AVCapturePhotoOutput?
    var cameraPreviewLayer: AVCaptureVideoPreviewLayer?
    var image: UIImage?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        button.layer.cornerRadius = 25.0
        setupCaptureSession()
        setupDevice()
        setupInputOutput()
        setupPreviewLayer()
        startRunningCaptureSession()
        // Do any additional setup after loading the view.
        
    }
    
    func setupCaptureSession() {
        //preset session for taking photos in full resolution
        captureSession.sessionPreset = AVCaptureSession.Preset.photo
    }
    
    func setupDevice() {
        //getting the device that we will use to take pictures, (Ex. wide angle camera)
        let deviceDiscoverySession = AVCaptureDevice.DiscoverySession(deviceTypes: [AVCaptureDevice.DeviceType.builtInWideAngleCamera], mediaType: AVMediaType.video, position: AVCaptureDevice.Position.unspecified)
        //get list of devices that comply with search criteria in device discovery session
        let devices = deviceDiscoverySession.devices
        for device in devices {
            if device.position == AVCaptureDevice.Position.back {
                backCamera = device
            } else if device.position == AVCaptureDevice.Position.front {
                frontCamera = device
            }
        }
        currentCamera = backCamera
    }
    
    func setupInputOutput() {
        do {
            let captureDeviceInput = try AVCaptureDeviceInput(device: currentCamera!)
            //add inputs to capture session
            captureSession.addInput(captureDeviceInput)
            photoOutput = AVCapturePhotoOutput()
            photoOutput?.setPreparedPhotoSettingsArray([AVCapturePhotoSettings(format: [AVVideoCodecKey: AVVideoCodecType.jpeg])], completionHandler: nil)
            captureSession.addOutput(photoOutput!)
        } catch {
            print(error)
        }
    }
    
    func setupPreviewLayer() {
        cameraPreviewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
        cameraPreviewLayer?.videoGravity = AVLayerVideoGravity.resizeAspectFill
        cameraPreviewLayer?.connection?.videoOrientation = AVCaptureVideoOrientation.portrait
        cameraPreviewLayer?.frame = photo.frame
        self.view.layer.insertSublayer(cameraPreviewLayer!, at: 0)
    }
    
    @IBAction func flipCamera(_ sender: Any) {
        guard let currentCameraInput: AVCaptureInput = captureSession.inputs.first else {
            return
        }
        captureSession.removeInput(currentCameraInput)
        var newCamera: AVCaptureDevice! = nil
        if let input = currentCameraInput as? AVCaptureDeviceInput {
            if (input.device.position == .back) {
                newCamera = getCameraWithPosition(position: .front)
            } else {
                newCamera = getCameraWithPosition(position: .back)
            }
        }
        do {
            let newInput = try AVCaptureDeviceInput(device: newCamera)
            captureSession.addInput(newInput)
        } catch {
            print(error)
        }
    }
    
    //just finds device with certain position
    func getCameraWithPosition(position: AVCaptureDevice.Position) -> AVCaptureDevice? {
        let deviceDiscoverySession = AVCaptureDevice.DiscoverySession(deviceTypes: [AVCaptureDevice.DeviceType.builtInWideAngleCamera], mediaType: AVMediaType.video, position: AVCaptureDevice.Position.unspecified)
        let devices = deviceDiscoverySession.devices
        for device in devices {
            if device.position == position {
                return device
            }
        }
        return nil
    }
    
    func startRunningCaptureSession() {
        //start capturing data
        captureSession.startRunning()
    }
    
    @IBAction func takePhoto(_ sender: UIButton) {
        let settings = AVCapturePhotoSettings()
        photoOutput?.capturePhoto(with: settings, delegate: self)
    }
    
//    @IBAction func TakePhoto(_ sender: UIButton) {
//        imagePicker = UIImagePickerController();
//        imagePicker.sourceType = .camera;
//        imagePicker.allowsEditing = true;
//        imagePicker.delegate = self;
//        present(imagePicker,animated: true);
//    }
    
//    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
//        imagePicker.dismiss(animated: true, completion: nil)
//        Photo.image = info[.originalImage] as? UIImage
//    }
    
}

extension ViewController: AVCapturePhotoCaptureDelegate {
    func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?) {
        if let imageData = photo.fileDataRepresentation() {
            print(imageData)
            image = UIImage(data: imageData);
            let newImage = UIImage(cgImage: (image?.cgImage)!, scale: image!.scale, orientation: .leftMirrored)
            littleImage.image =  newImage
        }
    }
}

