import io
import json
from collections import Counter

import requests
import streamlit as st
from PIL import Image


@st.experimental_memo
def load_dataset():
    with open("logo_annotations.jsonl", "r") as f:
        return list(map(json.loads, f))


@st.experimental_memo
def load_types():
    dataset = load_dataset()
    return sorted(set(x["annotation_type"] for x in dataset))


@st.experimental_memo
def load_value_tags(annotation_type: str, min_count: int):
    dataset = load_dataset()
    counter = Counter(
        (
            x["annotation_value_tag"]
            for x in dataset
            if x["annotation_type"] == annotation_type
        )
    )
    return sorted(
        ((key, count) for key, count in counter.items() if count >= min_count),
        key=lambda x: x[1],
        reverse=True,
    )


def filter_dataset(dataset, annotation_type, annotation_value_tag):
    for item in dataset:
        if (
            item["annotation_type"] == annotation_type
            and item["annotation_value_tag"] == annotation_value_tag
        ):
            yield item


def get_image(item):
    image_url = f"https://world.openfoodfacts.org/images/products{item['source_image']}"
    y_min, x_min, y_max, x_max = item["bounding_box"]
    r = requests.get(
        "https://robotoff.openfoodfacts.org/api/v1/images/crop",
        params={
            "image_url": image_url,
            "x_min": x_min,
            "y_min": y_min,
            "x_max": x_max,
            "y_max": y_max,
        },
    )
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content))


dataset = load_dataset()
count = int(st.number_input("Count", value=30, step=1))
min_value_count = int(st.number_input("Min value count", value=10, step=1))
logo_type = st.selectbox("Type", options=load_types())

if logo_type:
    logo_value, _ = st.selectbox(
        "Value",
        options=load_value_tags(logo_type, min_value_count),
        format_func=lambda x: f"{x[0]} ({x[1]})" if x[0] else f"<EMPTY> ({x[1]})",
    )

    if logo_value:
        filtered_logos = list(filter_dataset(dataset, logo_type, logo_value))

        st.write(f"{len(filtered_logos)} logos")
        logos_to_display = filtered_logos[:count]
        images = [get_image(logo) for logo in logos_to_display]
        st.image(images)
