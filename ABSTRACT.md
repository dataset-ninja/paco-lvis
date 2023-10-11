The authors introduce the **PACO-LVIS** dataset, strategically selecting vocabularies for objects, parts, and attributes by leveraging the strengths of the LVIS dataset. They identified 75 common object categories shared between both datasets, chose 200 parts classes from web-mined data, which expanded to 456 when accounting for object-specific parts. Additionally, a user study helped define a comprehensive set of 29 colors, 10 patterns, 13 materials, and 3 levels of reflectance attributes to enhance the dataset's object recognition and understanding capabilities.


## Image sources

PACO is constructed from [LVIS](https://ieeexplore.ieee.org/document/8954457) in the image domain (current dataset) and [Ego4D](https://arxiv.org/abs/2110.07058) in the video domain. Authors chose LVIS due to its large object vocabulary and federated dataset construction. Ego4D has temporally aligned narrations, making it easy to source frames corresponding to specific objects.

## Object vocabulary selection

Authors first mined all object categories mentioned in the narrations accompanying Ego4D and took the intersection with
common and frequent categories in LVIS. Authors then chose
categories with at-least 20 instances in Ego4D, resulting in
75 categories commonly found in both LVIS and Ego4D.

## Parts vocabulary selection

Excluding specific domains like fashion [20], there is no exhaustive ontology of parts for common objects. Authors mined part names from web-images obtained through queries like “parts of a car”. These images list part-names along with illustrations and pointers to the parts in the object. Authors manually curate such mined part names for an object category to only retain parts that are visible in majority of the object instances and clearly distinguishable. More details in the appendix. This resulted in a total of 200 part classes shared across all 75 objects. When expanded to object-specific parts this results in 456 object-part classes.

## Attribute vocabulary selection

Attributes are particularly useful in distinguishing different instances of the same object type. Motivated by this, authors conducted an in-depth user study (details in appendix) to identify the sufficient set of attributes that can separate all object instances in the dataset. This led to the final vocabulary of 29 colors, 10 patterns and markings, 13 materials and 3 levels of reflectance.

<img src="https://i.ibb.co/xSjfNk2/Screenshot-2023-10-11-132738.png" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;"> (left) PACO includes objects with object masks, object attributes, part masks, and part attributes. (right) Object instance queries composed of object and part attributes are shown with corresponding positive images in green and negative images in red.</span>
