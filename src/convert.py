import os
from collections import defaultdict
from urllib.parse import unquote, urlparse

import numpy as np
import pycocotools.mask as mask_util
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_name
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(
                        team_id, teamfiles_path, local_path, progress_cb=pbar
                    )

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "archive"
    # train_images_path = "/home/alex/DATASETS/TODO/PACO-LVIS/archive/train2017"
    # val_images_path = "/home/alex/DATASETS/TODO/PACO-LVIS/archive/val2017"
    # test_images_path = "/home/alex/DATASETS/DONE/LVIS/test2017"
    train_json_path = os.path.join("archive", "annotations", "paco_lvis_v1_train.json")
    val_json_path = os.path.join("archive", "annotations", "paco_lvis_v1_val.json")
    test_json_path = os.path.join("archive", "annotations", "paco_lvis_v1_test.json")
    batch_size = 10

    bad_data = [
        "train2017/000000563746.jpg",
        "train2017/000000500853.jpg",
        "train2017/000000280819.jpg",
        "train2017/000000112240.jpg",
        "train2017/000000261026.jpg",
        "train2017/000000476455.jpg",
        "train2017/000000341132.jpg",
        "train2017/000000425569.jpg",
        "train2017/000000457943.jpg",
        "train2017/000000319055.jpg",
        "train2017/000000306395.jpg",
        "train2017/000000551581.jpg",
        "train2017/000000557422.jpg",
        "train2017/000000289618.jpg",
        "train2017/000000326959.jpg",
        "train2017/000000166948.jpg",
        "train2017/000000078858.jpg",
        "train2017/000000318200.jpg",
        "train2017/000000261563.jpg",
        "train2017/000000278550.jpg",
        "train2017/000000235491.jpg",
        "train2017/000000157955.jpg",
        "train2017/000000454209.jpg",
        "train2017/000000524382.jpg",
        "train2017/000000179441.jpg",
        "train2017/000000113672.jpg",
        "train2017/000000113672.jpg",
        "train2017/000000546670.jpg",
        "train2017/000000429497.jpg",
        "train2017/000000545124.jpg",
        "train2017/000000514456.jpg",
        "train2017/000000534694.jpg",
        "train2017/000000187447.jpg",
        "train2017/000000131697.jpg",
        "train2017/000000130538.jpg",
        "train2017/000000329035.jpg",
        "train2017/000000323479.jpg",
        "train2017/000000498218.jpg",
        "train2017/000000489186.jpg",
        "train2017/000000226658.jpg",
        "train2017/000000123539.jpg",
        "train2017/000000248031.jpg",
        "train2017/000000006465.jpg",
        "train2017/000000064800.jpg",
        "train2017/000000045026.jpg",
        "train2017/000000474026.jpg",
        "train2017/000000475485.jpg",
        "train2017/000000434067.jpg",
        "train2017/000000216952.jpg",
        "train2017/000000363455.jpg",
        "train2017/000000328088.jpg",
        "train2017/000000106817.jpg",
        "train2017/000000200138.jpg",
        "train2017/000000216740.jpg",
        "train2017/000000287312.jpg",
        "train2017/000000542818.jpg",
        "train2017/000000509419.jpg",
        "train2017/000000453605.jpg",
        "train2017/000000018214.jpg",
        "train2017/000000135278.jpg",
        "train2017/000000123920.jpg",
        "train2017/000000351729.jpg",
        "train2017/000000115404.jpg",
        "train2017/000000044625.jpg",
        "train2017/000000422008.jpg",
        "train2017/000000205440.jpg",
        "train2017/000000238535.jpg",
        "train2017/000000110723.jpg",
        "train2017/000000139500.jpg",
        "train2017/000000242203.jpg",
        "train2017/000000279530.jpg",
        "train2017/000000231899.jpg",
        "train2017/000000049199.jpg",
        "train2017/000000513768.jpg",
        "train2017/000000472607.jpg",
        "train2017/000000098205.jpg",
        "val2017/000000359540.jpg",
        "val2017/000000507015.jpg",
        "val2017/000000570834.jpg",
        "train2017/000000048332.jpg",
        "train2017/000000235747.jpg",
        "train2017/000000373373.jpg",
        "train2017/000000250035.jpg",
        "train2017/000000335144.jpg",
        "train2017/000000317208.jpg",
        "train2017/000000467076.jpg",
    ]
    attributes_values = [
        "black",
        "light_blue",
        "blue",
        "dark_blue",
        "light_brown",
        "brown",
        "dark_brown",
        "light_green",
        "green",
        "dark_green",
        "light_grey",
        "grey",
        "dark_grey",
        "light_orange",
        "orange",
        "dark_orange",
        "light_pink",
        "pink",
        "dark_pink",
        "light_purple",
        "purple",
        "dark_purple",
        "light_red",
        "red",
        "dark_red",
        "white",
        "light_yellow",
        "yellow",
        "dark_yellow",
        "other(color)",
        "plain",
        "striped",
        "dotted",
        "checkered",
        "woven",
        "studded",
        "perforated",
        "floral",
        "other(pattern_marking)",
        "logo",
        "text",
        "stone",
        "wood",
        "rattan",
        "fabric",
        "crochet",
        "wool",
        "leather",
        "velvet",
        "metal",
        "paper",
        "plastic",
        "glass",
        "ceramic",
        "other(material)",
        "opaque",
        "translucent",
        "transparent",
        "other(transparency)",
    ]

    object_classes = [
        "trash_can",
        "handbag",
        "ball",
        "basket",
        "bicycle",
        "book",
        "bottle",
        "bowl",
        "can",
        "car_(automobile)",
        "carton",
        "cellular_telephone",
        "chair",
        "cup",
        "dog",
        "drill",
        "drum_(musical_instrument)",
        "glass_(drink_container)",
        "guitar",
        "hat",
        "helmet",
        "jar",
        "knife",
        "laptop_computer",
        "mug",
        "pan_(for_cooking)",
        "plate",
        "remote_control",
        "scissors",
        "shoe",
        "slipper_(footwear)",
        "stool",
        "table",
        "towel",
        "wallet",
        "watch",
        "wrench",
        "belt",
        "bench",
        "blender",
        "box",
        "broom",
        "bucket",
        "calculator",
        "clock",
        "crate",
        "earphone",
        "fan",
        "hammer",
        "kettle",
        "ladder",
        "lamp",
        "microwave_oven",
        "mirror",
        "mouse_(computer_equipment)",
        "napkin",
        "newspaper",
        "pen",
        "pencil",
        "pillow",
        "pipe",
        "pliers",
        "plastic_bag",
        "scarf",
        "screwdriver",
        "soap",
        "sponge",
        "spoon",
        "sweater",
        "tape_(sticky_cloth_or_paper)",
        "telephone",
        "television_set",
        "tissue_paper",
        "tray",
        "vase",
    ]
    part_categories = [
        "antenna",
        "apron",
        "arm",
        "back",
        "back_cover",
        "backstay",
        "bar",
        "barrel",
        "base",
        "base_panel",
        "basket",
        "bezel",
        "blade",
        "body",
        "border",
        "bottom",
        "bowl",
        "bracket",
        "bridge",
        "brush",
        "brush_cap",
        "buckle",
        "bulb",
        "bumper",
        "button",
        "cable",
        "camera",
        "canopy",
        "cap",
        "capsule",
        "case",
        "clip",
        "closure",
        "colied_tube",
        "control_panel",
        "cover",
        "cuff",
        "cup",
        "decoration",
        "dial",
        "door_handle",
        "down_tube",
        "drawer",
        "drawing",
        "ear",
        "ear_pads",
        "embroidery",
        "end_tip",
        "eraser",
        "eye",
        "eyelet",
        "face",
        "face_shield",
        "fan_box",
        "fender",
        "ferrule",
        "finger_hole",
        "fingerboard",
        "finial",
        "flap",
        "food_cup",
        "foot",
        "footrest",
        "fork",
        "frame",
        "fringes",
        "gear",
        "grille",
        "grip",
        "hand",
        "handle",
        "handlebar",
        "head",
        "head_tube",
        "headband",
        "headlight",
        "headstock",
        "heel",
        "hem",
        "hole",
        "hood",
        "housing",
        "inner_body",
        "inner_side",
        "inner_wall",
        "insole",
        "jaw",
        "joint",
        "key",
        "keyboard",
        "label",
        "lace",
        "lead",
        "left_button",
        "leg",
        "lid",
        "light",
        "lining",
        "logo",
        "loop",
        "lower_bristles",
        "lug",
        "mirror",
        "motor",
        "mouth",
        "neck",
        "neckband",
        "nose",
        "nozzle",
        "nozzle_stem",
        "outer_side",
        "outsole",
        "page",
        "pedal",
        "pedestal_column",
        "pediment",
        "pickguard",
        "pipe",
        "pom_pom",
        "prong",
        "pull_tab",
        "punt",
        "push_pull_cap",
        "quarter",
        "rail",
        "right_button",
        "rim",
        "ring",
        "rod",
        "roll",
        "roof",
        "rough_surface",
        "runningboard",
        "saddle",
        "screen",
        "screw",
        "scroll_wheel",
        "seal_ring",
        "seat",
        "seat_stay",
        "seat_tube",
        "shade",
        "shade_cap",
        "shade_inner_side",
        "shaft",
        "shank",
        "shelf",
        "shoulder",
        "side",
        "side_button",
        "sign",
        "sipper",
        "skirt",
        "sleeve",
        "slider",
        "spindle",
        "splashboard",
        "spout",
        "steeringwheel",
        "stem",
        "step",
        "sticker",
        "stile",
        "strap",
        "stretcher",
        "string",
        "switch",
        "swivel",
        "table_top",
        "tail",
        "taillight",
        "tank",
        "tapering_top",
        "teeth",
        "terry_bar",
        "text",
        "throat",
        "time_display",
        "tip",
        "toe_box",
        "tongue",
        "top",
        "top_cap",
        "top_tube",
        "touchpad",
        "trunk",
        "turnsignal",
        "turntable",
        "vamp",
        "vapour_cover",
        "visor",
        "welt",
        "wheel",
        "window",
        "windowpane",
        "windshield",
        "wiper",
        "wire",
        "yoke",
        "zip",
    ]

    errors = []
    color = sly.TagMeta("color", sly.TagValueType.ANY_STRING)
    pattern_making = sly.TagMeta("pattern making", sly.TagValueType.ANY_STRING)
    material = sly.TagMeta("material", sly.TagValueType.ANY_STRING)
    transparency = sly.TagMeta("transparency", sly.TagValueType.ANY_STRING)

    def index_to_attribute(index):
        if index in range(30):
            return "color"
        elif index in range(30, 41):
            return "pattern marking"
        elif index in range(41, 55):
            return "material"
        elif index in range(55, 59):
            return "transparency"

    def create_ann(image_path):
        labels = []
        tags = []

        image_name = image_path.split("/")[-2] + "/" + image_path.split("/")[-1]
        image_shape = image_name_to_shape.get(image_name)
        if image_shape is None:
            image_np = sly.imaging.image.read(image_path)[:, :, 0]
            img_height = image_np.shape[0]
            img_wight = image_np.shape[1]
        else:
            img_height = image_shape[0]
            img_wight = image_shape[1]

        ann_data = image_name_to_ann_data[image_name]
        for curr_ann_data in ann_data:
            label_tags = []
            attributes_idxs = curr_ann_data[3]
            group_to_value = {
                "color": [],
                "pattern marking": [],
                "material": [],
                "transparency": [],
            }
            for attribute_id in attributes_idxs:
                attributes_value = attributes_values[attribute_id]
                group_to_value[index_to_attribute(attribute_id)].append(
                    attributes_value
                )
            for tag_name, tag_values in group_to_value.items():
                if len(tag_values) == 0:
                    continue
                tag_meta = meta.get_tag_meta(tag_name)
                tag_value = ", ".join(tag_values)
                tag = sly.Tag(tag_meta, value=tag_value)
                label_tags.append(tag)

            category_id = curr_ann_data[0]
            class_name = category_to_class[category_id][0]
            obj_class = meta.get_obj_class(class_name)
            is_part_of = category_to_class[category_id][1]
            if is_part_of is not None:
                tag_part_of = sly.Tag(part_of, value=is_part_of)
                label_tags.append(tag_part_of)
            polygons_coords = curr_ann_data[1]
            if type(polygons_coords) is dict:
                mask = mask_util.decode(polygons_coords)
                # ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
                # for i in range(1, ret):
                #     obj_mask = curr_mask == i
                if len(np.unique(mask)) == 1:
                    errors.append(image_name)
                    continue
                curr_bitmap = sly.Bitmap(mask)
                # if curr_bitmap.area > 30:
                curr_label = sly.Label(curr_bitmap, obj_class, tags=label_tags)
                labels.append(curr_label)
            else:
                for coords in polygons_coords:
                    exterior = []
                    for i in range(0, len(coords), 2):
                        exterior.append([int(coords[i + 1]), int(coords[i])])
                    if len(exterior) < 3:
                        errors.append(image_name)
                        continue
                    poligon = sly.Polygon(exterior)
                    label_poly = sly.Label(poligon, obj_class, tags=label_tags)
                    labels.append(label_poly)

            bbox_coord = curr_ann_data[2]
            rectangle = sly.Rectangle(
                top=int(bbox_coord[1]),
                left=int(bbox_coord[0]),
                bottom=int(bbox_coord[1] + bbox_coord[3]),
                right=int(bbox_coord[0] + bbox_coord[2]),
            )
            label_rectangle = sly.Label(rectangle, obj_class, tags=label_tags)
            labels.append(label_rectangle)

        return sly.Annotation(
            img_size=(img_height, img_wight), labels=labels, img_tags=tags
        )

    color = sly.TagMeta("color", sly.TagValueType.ANY_STRING)
    pattern_making = sly.TagMeta("pattern marking", sly.TagValueType.ANY_STRING)
    material = sly.TagMeta("material", sly.TagValueType.ANY_STRING)
    transparency = sly.TagMeta("transparency", sly.TagValueType.ANY_STRING)
    part_of = sly.TagMeta("part of", sly.TagValueType.ANY_STRING)

    project = api.project.create(
        workspace_id, project_name, change_name_if_conflict=True
    )
    meta = sly.ProjectMeta(
        tag_metas=[color, pattern_making, material, transparency, part_of]
    )
    for obj_class_name in object_classes + part_categories:
        obj_class = meta.get_obj_class(obj_class_name)
        if obj_class is None:
            obj_class = sly.ObjClass(obj_class_name, sly.AnyGeometry)
            meta = meta.add_obj_class(obj_class)
    api.project.update_meta(project.id, meta.to_json())

    ds_to_data = {
        "val2017": val_json_path,
        "train2017": train_json_path,
        "test2017": test_json_path,
    }

    for ds_name, ann_path in ds_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)
        image_id_to_name = {}
        image_name_to_ann_data = defaultdict(list)
        image_name_to_shape = {}
        category_to_class = {}

        ann = load_json_file(ann_path)

        for curr_category in ann["categories"]:
            if curr_category["supercategory"] == "OBJECT":
                class_name = curr_category["name"]
                parent_name = None
            else:
                class_name = curr_category["synset"]
                parent_name = curr_category["name"].split(":")[0]
            category_to_class[curr_category["id"]] = (class_name, parent_name)
            # if idx_to_obj_class.get(curr_category["id"]) is None:
            #     obj_class = sly.ObjClass(curr_category["name"], sly.AnyGeometry)
            #     meta = meta.add_obj_class(obj_class)
            #     idx_to_obj_class[curr_category["id"]] = obj_class
        # api.project.update_meta(project.id, meta.to_json())

        for curr_image_info in ann["images"]:
            image_name = (
                curr_image_info["coco_url"].split("/")[-2]
                + "/"
                + curr_image_info["coco_url"].split("/")[-1]
            )
            image_id_to_name[curr_image_info["id"]] = image_name
            image_name_to_shape[image_name] = (
                curr_image_info["height"],
                curr_image_info["width"],
            )

        for curr_ann_data in ann["annotations"]:
            image_id = curr_ann_data["image_id"]
            image_name_to_ann_data[image_id_to_name[image_id]].append(
                [
                    curr_ann_data["category_id"],
                    curr_ann_data["segmentation"],
                    curr_ann_data["bbox"],
                    curr_ann_data["attribute_ids"],
                ]
            )

        images_names = list(image_name_to_shape.keys())

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(dataset_path, image_name) for image_name in img_names_batch
            ]

            img_names_batch = [im_name.split("/")[-1] for im_name in img_names_batch]

            img_infos = api.image.upload_paths(
                dataset.id, img_names_batch, images_pathes_batch
            )
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))
    print(errors)
    return project
