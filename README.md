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
+ [Usage](#usage-)
  
---

## Academic Work 📖

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

<img width="30%" height="30%" alt="image" src="https://github.com/user-attachments/assets/ed551f19-e74c-4eb0-81f4-8f877583a193" />

---

## Features ✔️
This section summarizes the features available in the application.

### Image Segmentation Methods
Segmentation is a process in Image Processing that aims to separate the regions of interest in an image from the rest. This resulting image is called a _mask_.

#### Frame Difference 
This method consists of subtracting and combining the differences between the current frame and its previous and subsequent frames, resulting in images such as the following example:

<img width="484" height="271" alt="image" src="https://github.com/user-attachments/assets/e53de431-7bbf-475e-b542-373304e997be" />

#### Median Background

This method creates a background model based on the median of a set of frames in the video. In a scenario where we cannot fully see the background in any single frame, the effect may look like the following example: 

<img width="486" height="270" alt="image" src="https://github.com/user-attachments/assets/62a37f10-9146-45a4-a8b6-6ba50149b66f" />

With this model, it is possible to subtract it from the video frames, resulting in a new segmented image:

<img width="486" height="269" alt="image" src="https://github.com/user-attachments/assets/7231c4e1-edd8-4702-a641-2ad33759f70c" />

---

### Frame Filtering

Before processing the images for segmentation, it is important to filter the frames to eliminate noise and make processing easier. For that, bilateral filtering is applied (you can see more about it [here](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html) in the OpenCV documentation), and the colors are also converted to grayscale. 

---

### Morphological Operations

These types of operations are applied to the "shape" of pixel regions in a way that enhances or refines aspects of an image. In this case, the software uses erosion and dilation. For example, if you apply dilation to an image with thin lines, the lines will become thicker, as in the following example:

<img width="487" height="264" alt="image" src="https://github.com/user-attachments/assets/1f46a200-dea2-4593-b194-b5f893f67acb" />

---

### Frame Separation

A video is nothing more than a sequence of images; each image is called a frame. The application first separates the frames of the video for further processing.

---

### Individual Folders for Each Operation

For each operation, there is a corresponding folder. This is useful for individual analysis of the results. You can also easily save the folders to another location on your machine, organized as shown in the following image: 

<img width="349" height="467" alt="image" src="https://github.com/user-attachments/assets/dfcffc20-4eb7-45b9-8d90-a82b5648eeca" />

_English Captions:_
+ _Raiz_: Root  
+ _Frame_mediano_: Median Frame  
+ _Frames_Extraidos_: Extracted Frames  
+ _Mascaras_FrameDiff_: Frame Difference Masks  
+ _Mascaras_Mediana_: Median Masks  

---

## Software Development

If you are interested in the software architecture, this section is for you. It briefly describes the main parts of the application. For more diagrams and algorithms, see my paper in the [Academic Work](#academical-work-) section. 

The following diagram represents the relationship between the Python modules in the application:

<img width="70%" height="70%" alt="image" src="https://github.com/user-attachments/assets/d8266271-c1a5-4de5-b16f-a1e0e6eb5a6d" />

Each module's function can be described as follows:

+ **cv2**: OpenCV library  
+ **os**: Operating system functions  
+ **shutil**: High-level file operations  
+ **numpy**: Mathematical operations  
+ **tkinter**: Graphical user interface  
+ **fileManager**: Manages the project files, such as images, videos, and folders  
+ **videoProcessing**: Uses OpenCV for video processing  
+ **imageProcessing**: Uses OpenCV for frame processing  
+ **window**: User interface  
+ **run**: Starts the application by calling the window module  

The main flow of the segmentation algorithm can be described by the following diagram:

<img width="50%" height="50%" alt="Cópia do FluxoSgmentação(ENG) drawio(1)" src="https://github.com/user-attachments/assets/f0affa6e-e88d-48e5-8e60-ca5749af186e" />

---

## Usage 🔬

---

⚠️ First, it is extremely important that any video used in the software be captured with a stable, immobilized camera. This is required because all methods are based on motion.

---
In the software's root path, type in the console:

```
python run.py
```

this will open the main application window.


This section explains the software use case, following the numbering shown in the image:

<img width="674" height="488" alt="image" src="https://github.com/user-attachments/assets/50553bc3-2b7a-4223-bedb-7eb875b597e6" />

### Interface Legend (Portuguese → English) 🖥️ 

| Nº | Category | Portuguese | English |
|----|----------|------------|---------|
| — | Section | Processamento de vídeo | Video Processing |
| — | Section | Pré-Processamento | Pre-Processing |
| — | Section | Processamento | Processing |
| — | Section | Arquivos | Files |
| 1 | Action | Selecionar vídeo | Select video |
| — | Status | Nenhum vídeo selecionado | No video selected |
| 2 | Action | Extrair Frames | Extract Frames |
| 3 | Action | Aplicar Filtros | Apply Filters |
| 4 | Processing Method | Fundo mediano | Median background |
| 4 | Processing Method | Diferença de Frames | Frame differencing |
| 5 | Post-processing (Morphology) | Dilatar | Dilation |
| 5 | Post-processing (Morphology) | Erodir | Erosion |
| 6 | Action | Aplicar método | Apply method |
| 7 | Action | Operação morfológica | Morphological operation |
| 8 | File | frames_extraidos | extracted_frames |
| 8 | File | frame_mediano | median_frame |
| 8 | File | binarizacao_gray | gray_binarization |
| 8 | File | mascaras_FrameDiff | frame_diff_masks |
| 8 | File | mascaras_mediana | median_masks |
| 9 | Action | Salvar Cache | Save Cache |
| 10 | Action | Limpar Cache | Clear Cache |

### Use Case

Following the order presented in the figure, the use case narrative is described below:

1. The user must choose a video file.  
2. Once the file is selected, the video frames must be extracted.  
3. With the frames extracted, filters can be applied.  
4. The user then selects the processing method, either **median background** or **frame differencing**.  
5. At this point (not mandatory), the user may select a post-processing method using morphological operations, either **dilation** or **erosion**.  
6. The method selected in step 4 is applied.  
7. Only after a method has been applied in step 6 may the user perform post-processing using the method chosen in step 5.  
8. The user selects which files should be saved.  
9. Based on the selected files, they are saved to a directory chosen through the file explorer.
