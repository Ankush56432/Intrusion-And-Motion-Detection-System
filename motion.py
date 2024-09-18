import cv2
import numpy as np

# Initialize global variables
draw = False
a, b = -1, -1
rect = (0, 0, 0, 0)
frame1 = None

def click_event(event, x, y, flags, param):
    global draw, a, b, frame1, rect

    # When left button is pressed down, start drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        a, b = x, y
        draw = True

    # When mouse is moving and drawing is active, display rectangle
    elif event == cv2.EVENT_MOUSEMOVE:
        if draw:
            temp_frame = frame1.copy()
            cv2.rectangle(temp_frame, (a, b), (x, y), (0, 0, 255), 2)
            cv2.imshow("frame", temp_frame)

    # When left button is released, finalize the rectangle
    elif event == cv2.EVENT_LBUTTONUP:
        draw = False
        cv2.rectangle(frame1, (a, b), (x, y), (0, 0, 255), 2)
        rect = (a, b, x, y)  # Store the final rectangle coordinates
        cv2.imshow("frame", frame1)

def main():
    global frame1, rect
   
    cap = cv2.VideoCapture("indian army.mp4")

    # Read the first frame
    ret, frame1 = cap.read()
    if not ret:
        print("Failed to read the video.")
        return

    # Read the second frame for comparison
    ret, frame2 = cap.read()
    if not ret:
        print("Failed to read the second frame.")
        return

    # Set the region of interest to the whole frame initially
    rect = (0, 0, frame1.shape[1], frame1.shape[0])
    
    # Display the first frame and set up the mouse callback
    cv2.imshow("frame", frame1)
    cv2.setMouseCallback('frame', click_event)
    cv2.waitKey(0)  # Wait for user to draw the rectangle and press a key

    while cap.isOpened():
        # Calculate the difference between two frames
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)

        # Ensure rect boundaries are valid (handling negative or out-of-bounds indices)
        x1, y1, x2, y2 = rect
        x1, x2 = max(0, min(x1, x2)), min(frame1.shape[1], max(x1, x2))
        y1, y2 = max(0, min(y1, y2)), min(frame1.shape[0], max(y1, y2))
        
        crop = dilated[y1:y2, x1:x2]  # Crop the region of interest based on rect
        cv2.imshow("mask", dilated)

        # Find contours within the cropped area
        contours, _ = cv2.findContours(crop, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.rectangle(frame1, (x1, y1), (x2, y2), (0, 0, 255), 2)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 900:  # Ignore small contours
                continue
            cv2.rectangle(frame1, (x1 + x, y1 + y), (x1 + x + w, y1 + y + h), (0, 255, 0), 2)
            cv2.putText(frame1, "Intruder Not Found", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # Show the updated frame
        cv2.imshow("feed", frame1)

        # Prepare for the next frame
        frame1 = frame2
        ret, frame2 = cap.read()

        if not ret:
            break  # Break the loop if no more frames are available

        # Break loop on 'ESC' key press
        if cv2.waitKey(40) == 27:
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
