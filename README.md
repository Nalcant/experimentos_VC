# A Tool for Video Segmentation Methods 👁️

"Experimentos_VC" (_eng: Experiments_CV_) is my personal public repository for my academic research in the field of Computer Vision.
The beginning (and main study case) of this research is related to the application of image segmentation methods for tracking the activity of paramedics inside ambulances.

The current goal achieved here was the segmentation of nurses during medical training in an environment that lacks control over variables that influence Image Processing operations, such as light stability.  
This software was developed using **Python and OpenCV**, a Computer Vision library whose documentation you can check [here](https://docs.opencv.org/4.x/index.html).

---

## Sumary:
+ [Academical Work](#academical-work-)
+ [Introduction to Computer Vision and Image Sementation (for Dummies)](#introduction-to-computer-vision-and-image-segmentation-for-dummies-%EF%B8%8F)
+ [Features](#features-%EF%B8%8F)
+ [Software Development](#software-development)
  
---

## Academical Work 📖

This README.md document is focused on presenting the application and its features, while also giving a short introduction to the topic for newcomers, rather than going deeper into the theory of the currently applied methods.  
If you are interested in that part, I invite you to take a look at my academic paper:

["_Segmentação de imagens para identificação de paramédicos em ambulâncias_"](https://github.com/user-attachments/files/24966900/alcantara_nm_tcc_bauru_sub.pdf)

It is available only in Brazilian Portuguese; however, you will find good reference material in English in the final **"Referências"** (_eng: References_) section.

---

## Introduction to Computer Vision and Image Segmentation (for Dummies ☝️🤓)

If you are not from the field and are just passing by, this section is for you. First, it is necessary to answer: 
##  What is Computer Vision?

Every time a machine needs to identify, infer, track, or perform any action that attempts to **mimic human visual cognition**, we can say we have a Computer Vision problem to solve. This includes, for example, applications in public and private security, medical image diagnosis, robotics, and more.

![wicv2](https://github.com/user-attachments/assets/11b7b5aa-d79f-4f75-bd32-3f2a1026a706)

## But what about Image Processing?

Image Processing often blurs the thin line that differentiates it from Computer Vision. This occurs because Image Processing operations are necessary steps to achieve Computer Vision tasks.

Of course, just like AI systems do not really "think" (a very fun philosophical question to discuss), a computer processing a Computer Vision system does not actually *see*, at least not in the same way humans do.  
We, as human beings, can correlate a series of information from a scene just by looking at it. For example, at the moment I write this, I have no difficulty describing every item on my desk. For a computer, however, this is a very challenging task.

To understand why computers have a hard time understanding images, it is necessary to remember what images really are: a set of pixels organized in a matrix and displayed on your screen. In the end, the computer only has color values and positions to deal with. Take as an example a pixel matrix where one means white and zero means black:

<img width="461" height="195" alt="image" src="https://github.com/user-attachments/assets/ecc4286c-2129-4499-836a-a884c044aa07" />

Therefore, **Image Processing methods are used to analyze, classify, and manipulate the pixels of an image so that we can abstract visual information from them.** Take as an example the image processing techniques applied to the popular photo of the model Lena:

<img width="50%" height="50%" alt="image" src="https://github.com/user-attachments/assets/ed551f19-e74c-4eb0-81f4-8f877583a193" />

---

## Features ✔️
This section resume the features available in the application

### Image Segmentation Methods
Segmatation is a process in Image Processing  that aims to separate the zones of interest of an image from the rest
#### Frame Difference 
This method consists in subtracting and joining the differences between the current frame with his previous and posterior frames, resulting in images such as the following exemple:


<img width="484" height="271" alt="image" src="https://github.com/user-attachments/assets/e53de431-7bbf-475e-b542-373304e997be" />

#### Median Background

This methods creates a model of a background, based on the median of a set of frames in the video, in a scenario that we cant fully see the background in any frame, the effect can look like the following exemple: 

<img width="486" height="270" alt="image" src="https://github.com/user-attachments/assets/62a37f10-9146-45a4-a8b6-6ba50149b66f" />

---





### Frame Filtering 

### Frame separation

### Individual folder for each opearation


---

## Software Development

If you are interested in the software architeture, this section is for you, it will describe shortly the main parts of the application, for more diagrams and algorithms, see my paper in the [Academical Work](#academical-work-) section. 


The following diagram represents the relation between the python modules in the application:


<img width="70%" height="70%" alt="image" src="https://github.com/user-attachments/assets/d8266271-c1a5-4de5-b16f-a1e0e6eb5a6d" />

Each module function can be described as the following:

+ cv2: OpenCV2 library
+ os: Operation System functions
+ shutil: High level file operations
+ numpy: Math operations
+ tkinter: Graphical Interface
+ fileManager: Manage te files of the project, such as images, videos and folders
+ videoProcessing: Utilizes OpenCV to video processing
+ imageProcessing: Utilizes OpenCV to frame processing
+ window: User interface
+ run: Starts the application calling window module

The main flux of the segmentation methods algorithm can be described by the following diagram:


<img width="50%" height="50%" alt="Cópia do FluxoSgmentação(ENG) drawio(1)" src="https://github.com/user-attachments/assets/f0affa6e-e88d-48e5-8e60-ca5749af186e" />






