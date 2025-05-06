import math


class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 100:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids

# import math
# import cv2
# from deep_sort_realtime.deepsort_tracker import DeepSort


# class Tracker:
#     def __init__(self):
#         # Khởi tạo DeepSORT
#         self.tracker = DeepSort(max_age=30, n_init=3,
#                                 nms_max_overlap=1.0,
#                                 max_cosine_distance=0.4)

#     def update(self, frame, objects_rect_with_conf):
#         """
#         frame: khung hình hiện tại (numpy array)
#         objects_rect_with_conf: danh sách [x1, y1, x2, y2, conf, cls]
#         """

#         # Chuyển về định dạng DeepSORT yêu cầu: [bbox(x,y,w,h), conf, class_id]
#         detections = []
#         for r in objects_rect_with_conf:
#             x1, y1, x2, y2, conf, cls = r
#             w = x2 - x1
#             h = y2 - y1
#             detections.append(([x1, y1, w, h], conf, cls))

#         # Cập nhật tracker
#         tracks = self.tracker.update_tracks(detections, frame=frame)

#         # Kết quả trả về: danh sách [x1, y1, x2, y2, track_id]
#         tracked_objects = []
#         for track in tracks:
#             if not track.is_confirmed():
#                 continue
#             track_id = track.track_id
#             x1, y1, x2, y2 = map(int, track.to_ltrb())
#             tracked_objects.append([x1, y1, x2, y2, track_id])

#         return tracked_objects