# Project Title: AI-Driven Presentation Generator with Hand Gesture Control

## Description

The project consists of two main components: Hand gesture control and AI-generated presentations, along with the corresponding user interface (UI).

## User Interface

The UI is designed using HTML, CSS, JavaScript, and BootStrap. Navigation between the endpoints is facilitated using Python and Flask. The UI comprises four pages:
1. The homepage featuring "Create" and "Present" buttons
2. A form allowing users to input their preferences
3. A modal for downloading the generated presentation
4. A page for uploading the presentation to be delivered

## Hand Gesture Control

This feature involves the use of four main libraries:
1. os: Used for accessing the file system and reading file paths
2. cvzone: Used for hand tracking and based on OpenCV
3. cv2: Used for video processing and drawing on the frame
4. numpy: Used for numerical computing

## AI Generated Presentations

For implementing this aspect, a form is included for users to enter:
1. Presentation title
2. Presenter's name
3. Number of slides
4. Presentation content
5. Option to add images
6. Choice of template

This data is utilized to create a prompt for an AI model. The response generated is then parsed and used to design the presentation slides.
