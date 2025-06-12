from fastapi import FastAPI, WebSocket , WebSocketDisconnect
import asyncio
import cv2 as cv
import threading
from ultralytics import YOLO
import torch
import json
from fastapi.middleware.cors import CORSMiddleware
import base64
import numpy as np


model = YOLO('./best.pt')


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Global variables

running = False
thread = None
latest_predictions = None

@app.get("/")
async def get_root():
    ans = await worker()
    data = { 'class' : 'cat', 'prediction' : ans  }

    return data



@app.get("/start")
def get_start():
    global thread, running

    if not running :
        running = True
       # thread = threading.Thread(target=worker) 
       # thread.start()
        return {"status": "detection started"}
    
    else:
        return {"status" : "already running"}
    




@app.post("/stop")
def get_stop():
    global running
    
    running = False

    return {"status" : "stopping detection"}



# def worker():

#     global running, latest_predictions
    
#     capture = cv.VideoCapture(0)
#     while running :
#         isTrue, frame = capture.read()
        
#         if isTrue:
#             result = model(frame, imgsz=640, conf=0.6, iou=0.45)
#             annotated_frame = result[0].plot()
#             data = [(model.names[int(cls_id)], conf.item()) for r in result for cls_id, conf in zip(r.boxes.cls, r.boxes.conf)]
#             structured_data = []
#             for item in data:
#                 structured_data.append({
#                     "class_name": item[0],
#                     "confidence": item[1]
#                 })
           
#             latest_predictions =  structured_data #updating prediction
           
           
#         else:
#             print("Failed to capture frame")
#             break

#         if cv.waitKey(1) & 0xFF == ord('d'):
#             break
#     capture.release()
#     cv.destroyAllWindows()




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # accept the connection
    print("WebSocket client connected")

    try:
        while True:
            data = await websocket.receive_text()
            
            print(f"Received data length: {len(data)}")
            print(f"Data preview: {data[:100] if len(data) > 100 else data}")
            
            # Check if data is valid and contains base64 image
            if not data or len(data) < 100:
                print("Invalid or too small data received")
                await websocket.send_text(json.dumps({"error": "Data too small"}))
                continue
                
            if "," not in data:
                print("Invalid data format - no comma separator")
                await websocket.send_text(json.dumps({"error": "Invalid format"}))
                continue
            
            try:
                # Strip metadata from Base64 string (remove "data:image/jpeg;base64,")
                parts = data.split(",")
                if len(parts) < 2:
                    print("Invalid base64 format")
                    continue
                    
                encoded_data = parts[1]
                print(f"Base64 data length: {len(encoded_data)}")
                
                # Validate base64 data
                if len(encoded_data) < 100:
                    print("Base64 data too small")
                    continue
                
                # Decode base64
                try:
                    img_bytes = base64.b64decode(encoded_data)
                    print(f"Decoded bytes length: {len(img_bytes)}")
                except Exception as decode_error:
                    print(f"Base64 decode error: {decode_error}")
                    continue
                
                if len(img_bytes) == 0:
                    print("Empty image bytes after decoding")
                    continue

                # Convert to NumPy array
                np_arr = np.frombuffer(img_bytes, np.uint8)
                print(f"Numpy array length: {len(np_arr)}")
                
                if len(np_arr) == 0:
                    print("Empty numpy array")
                    continue

                # Decode image
                img = cv.imdecode(np_arr, cv.IMREAD_COLOR)

                # Check if image was decoded successfully
                if img is None:
                    print("Failed to decode image - cv.imdecode returned None")
                    continue

                if img.size == 0:
                    print("Empty image after decoding")
                    continue

                # Now you can process the frame with OpenCV
                print(f"SUCCESS! Received frame of size: {img.shape}")

                result = model(img, imgsz=640, conf=0.6, iou=0.45)

                data = [(model.names[int(cls_id)], conf.item()) for r in result for cls_id, conf in zip(r.boxes.cls, r.boxes.conf)]


                structured_data = []
                for item in data:
                    structured_data.append({
                        "class_name": item[0],
                        "confidence": item[1]
                })
           
  

                print(f"Sending {len(structured_data)} detections")
                # Send results back to client
                await websocket.send_text(json.dumps(structured_data))
                
            except Exception as e:
                print(f"Error processing frame: {e}")
                import traceback
                traceback.print_exc()
                await websocket.send_text(json.dumps({"error": str(e)}))
                continue
                
            # Small delay to prevent overwhelming
            await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        import traceback
        traceback.print_exc()


