**PACO-LVIS: Parts and Attributes of Common Objects - Large Vocabulary Instance Segmentation** is a dataset for instance segmentation, object detection, and semantic segmentation tasks. It is applicable or relevant across various domains. 

The dataset consists of 57643 images with 1644461 labeled objects belonging to 270 different classes including *body*, *rim*, *handle*, and other: *base*, *neck*, *side*, *inner_body*, *leg*, *bottom*, *back*, *strap*, *top*, *seat*, *wheel*, *inner_side*, *mirror*, *lid*, *bowl*, *blade*, *case*, *shoulder*, *pipe*, *screen*, *foot*, *button*, *cover*, *logo*, *bench*, and 242 more.

Images in the PACO-LVIS dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. All images are labeled (i.e. with annotations). There are 3 splits in the dataset: *train2017* (45790 images), *test2017* (9443 images), and *val2017* (2410 images). Also, the objects contains ***color***, ***pattern marking***, ***material***, ***transparency*** and ***part_of*** object tags. Explore them in the supervisely labeling tool. The dataset was released in 2023 by the Meta AI and Simon Fraser University, Canada.

Here is a visualized example for randomly selected sample classes:

[Dataset classes](https://github.com/dataset-ninja/paco-lvis/raw/main/visualizations/classes_preview.webm)
