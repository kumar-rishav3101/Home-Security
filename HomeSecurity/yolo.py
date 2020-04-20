import numpy as np
import cv2
from . import Media

def camera(number):
    camera = cv2.VideoCapture(0)
    send=0
    count=0
    h, w = None, None

    with open('F:\Study\Practise\Security\HomeSecurity\yolo-coco-data\coco.names') as f:
        labels = [line.strip() for line in f]

    network = cv2.dnn.readNetFromDarknet('F:\Study\Practise\Security\HomeSecurity\yolo-coco-data\yolov3.cfg',
                                         'F:\Study\Practise\Security\HomeSecurity\yolo-coco-data\yolov3.weights')

    layers_names_all = network.getLayerNames()

    layers_names_output = \
        [layers_names_all[i[0] - 1] for i in network.getUnconnectedOutLayers()]

    probability_minimum = 0.5

    threshold = 0.3

    colours = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

    while True:
        _, frame = camera.read()
        if w is None or h is None:
            h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        network.setInput(blob)
        output_from_network = network.forward(layers_names_output)


        bounding_boxes = []
        confidences = []
        class_numbers = []
        for result in output_from_network:

            for detected_objects in result:

                scores = detected_objects[5:]

                class_current = np.argmax(scores)

                confidence_current = scores[class_current]
                if confidence_current > probability_minimum:
                    box_current = detected_objects[0:4] * np.array([w, h, w, h])
                    x_center, y_center, box_width, box_height = box_current
                    x_min = int(x_center - (box_width / 2))
                    y_min = int(y_center - (box_height / 2))
                    bounding_boxes.append([x_min, y_min,
                                           int(box_width), int(box_height)])
                    confidences.append(float(confidence_current))
                    class_numbers.append(class_current)
        results = cv2.dnn.NMSBoxes(bounding_boxes, confidences,
                                   probability_minimum, threshold)

        if len(results) > 0:

            for i in results.flatten():
                object=labels[int(class_numbers[i])]
                if object == 'person':
                #if object == 'cell phone':
                    cv2.line(frame, (0,250), (1024,250), (0, 255, 0), 1)
                    print(y_min)
                    if y_min > 150:
                        count+=1
                    x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
                    box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]
                    colour_box_current = colours[class_numbers[i]].tolist()
                    cv2.rectangle(frame, (x_min, y_min),
                                  (x_min + box_width, y_min + box_height),
                                  colour_box_current, 2)
                    text_box_current = '{}: {:.4f}'.format(labels[int(class_numbers[i])],
                                                           confidences[i])
                    cv2.putText(frame, text_box_current, (x_min, y_min - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour_box_current, 2)
                    if send==0 and count==5:
                        Media.sms(number,frame)
                        send=1



        cv2.namedWindow('CAMERA ON', cv2.WINDOW_NORMAL)
        cv2.imshow('CAMERA ON', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
