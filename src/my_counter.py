import cv2
import numpy as np
from ultralytics import YOLO
from tracker import *


class MyObjectCounter:
    def __init__(self, model_path="yolov8n.pt", polygon1=None, polygon2=None, classes=[0], show=True):
        self.model = YOLO(model_path)
        self.tracker = Tracker()
        self.polygon1 = polygon1 if polygon1 else []
        self.polygon2 = polygon2 if polygon2 else []
        self.classes = classes
        self.show = show
        self.person_entering = {}
        self.person_exiting = {}
        self.entering = set()
        self.exiting = set()
    def is_inside_polygon(self, point, polygon):
        return cv2.pointPolygonTest(np.array(polygon, dtype=np.int32), point, False) >= 0

    def process_frame(self, frame):
        results = self.model(frame, classes=self.classes, verbose=False)[0]
        detections = []

        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = r
            detections.append([x1, y1, x2, y2])

        bbox_id = self.tracker.update(detections)
        
        for bbox in bbox_id:
            x3, y3, x4, y4, id = bbox
            x3, y3, x4, y4 = int(x3), int(y3), int(x4), int(y4)
            
            x0, y0 = x3, y3
            
            cx = int((x3 + x4) / 2)
            cy = int((y3 + y4) / 2)

            cv2.rectangle(frame, (x3, y3), (x4, y4), (125,125, 125), 2)
            cv2.putText(frame, f'{id}', (x3, y3),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0)  ,1)            

            if self.is_inside_polygon((x0, y0), self.polygon1):
                self.person_entering[id] = (x0, y0)
                cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 255), 2)
                cv2.circle(frame, (x0, y0 ), 5, (255, 0, 255), -1)
            if id in self.person_entering:
                if self.is_inside_polygon((x0, y0), self.polygon2):
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 0), 2)
                    cv2.circle(frame, (x0, y0 ), 5, (0, 0, 0), -1)
                    # cv2.putText(frame, f'{id}', (x3, y3),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0)  ,1)
                    self.entering.add(id)


            if self.is_inside_polygon((x0, y0), self.polygon2):
                self.person_exiting[id] = (x0, y0)
                cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                cv2.circle(frame, (x0, y0 ), 5, (255, 0, 255), -1)
            if id in self.person_exiting:
                if self.is_inside_polygon((x0, y0), self.polygon1):
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (255, 255, 0), 2)
                    cv2.circle(frame, (x0, y0 ), 5, (123, 123, 123), -1)
                    # cv2.putText(frame, f'{id}', (x3, y3),
                                # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0)  ,1)
                    self.exiting.add(id)
            
        if self.polygon1:
            cv2.polylines(frame, [np.array(self.polygon1, np.int32)], True, (0, 255, 255), 1)

        if self.polygon2:
            cv2.polylines(frame, [np.array(self.polygon2, np.int32)], True, (0, 255, 255), 1)
        cv2.putText(frame, f'People entering: {len(self.entering)}', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(frame, f'People exiting: {len(self.exiting)}', (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        if self.show:
            cv2.imshow("MyObjectCounter", frame)

        return frame

