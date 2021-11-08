#!/bin/sh

echo "Downloading Tensorflow models ..."
for asset_name in "tf-universal-logo-detector" "tf-nutrition-table" "tf-nutriscore"; do
    dir=`echo ${asset_name} | sed 's/tf-//g'`
    mkdir -p tf_models/${dir} tf_models/${dir}/1
    wget -cO - https://github.com/openfoodfacts/robotoff-models/releases/download/${asset_name}-1.0/label_map.pbtxt > tf_models/${dir}/labels.pbtxt
    wget -cO - https://github.com/openfoodfacts/robotoff-models/releases/download/${asset_name}-1.0/saved_model.tar.gz > tf_models/${dir}/1/saved_model.tar.gz
    tar -xzvf ${dir}/1/saved_model.tar.gz --strip-component=1 -C tf_models/${dir}/1
    rm ${dir}/1/saved_model.tar.gz
done;

echo "Downloading Keras Category Classifier ..."
base_url=https://github.com/openfoodfacts/robotoff-models/releases/download/keras-category-classifier-xx-1.0
dest_folder=models/category
mkdir -p ${dest_folder}
wget -cO - ${base_url}/config.json > ${dest_folder}/config.json
wget -cO - ${base_url}/category_taxonomy.json > ${dest_folder}/category_taxonomy.json
wget -cO - ${base_url}/category_voc.json > ${dest_folder}/category_voc.json
wget -cO - ${base_url}/ingredient_voc.json > ${dest_folder}/ingredient_voc.json
wget -cO - ${base_url}/product_name_voc.json > ${dest_folder}/product_name_voc.json
wget -cO - ${base_url}/checkpoint.hdf5 > ${dest_folder}/checkpoint.hdf5
