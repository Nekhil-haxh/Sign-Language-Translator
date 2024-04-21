import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera
from viam.services.vision import VisionClient
from speech_service_api import SpeechService

async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='qloltkj1ye9nmll7tism76cehepdvzwz',
        api_key_id='fa879a8a-a1c8-4137-97a0-3e04fc91811c'
    )
    return await RobotClient.at_address('sign-language-translator-2-0-main.ynjswnc7in.viam.cloud', opts)

async def main():
    machine = await connect()

    print('Resources:')
    print(machine.resource_names)
    
    speech = SpeechService.from_robot(machine, name="speech")
    
    while True:
        # Webcam
        webcam = Camera.from_robot(machine, "Webcam")
        webcam_return_value = await webcam.get_image()
        print(f"Webcam get_image return value: {webcam_return_value}")
      
        '''# csi
        csi = Camera.from_robot(machine, "csi")
        csi_return_value = await csi.get_image()
        print(f"csi get_image return value: {csi_return_value}")'''
      
        # Note that the Camera supplied is a placeholder. Please change this to a valid Camera. Also note that the get_classifications method is a placeholder and is commented out to give you a choice to use get_detections method instead if you are doing detections.
        # yolo
        yolo = VisionClient.from_robot(machine, "yolo")
        yolo_return_value = await yolo.get_detections_from_camera("Webcam")
        
        
        if yolo_return_value:
            confidence = yolo_return_value[0].confidence
            if confidence > 0.8:
                letter = (yolo_return_value[0].class_name)
                print(letter)
                text = await speech.say(letter, True)
        

    # Don't forget to close the machine when you're done!
    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
