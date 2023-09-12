#!/usr/bin/bash
source .env

ZIP_NAME="rendus/practice""$NUM_TP""_""$GROUP_NAME"".zip"
FILES_TO_EXCLUDE=(
    "**/__pycache__/*"
    "practice$NUM_TP/*.pdf"
)

EXCLUDED_FILES="-x "
for file in "${FILES_TO_EXCLUDE[@]}"
do
    EXCLUDED_FILES+="$file "
    echo -e "excluded file: $file\n"
done

zip "$ZIP_NAME" -r "practice$NUM_TP" $EXCLUDED_FILES

zipinfo "$ZIP_NAME"