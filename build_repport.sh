#!/usr/bin/bash
source .env

TAR_NAME="rendus/practice""$NUM_TP""_""$GROUP_NAME"".tar"
ZIP_NAME="rendus/practice""$NUM_TP""_""$GROUP_NAME"".tgz"

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

# Create a tar archive from the files to be included.
tar -cf "$TAR_NAME" "practice$NUM_TP" --exclude=${FILES_TO_EXCLUDE[0]//**/} --exclude=${FILES_TO_EXCLUDE[1]//**/}

# Compress the tar archive into a zip archive.
zip -9 "$ZIP_NAME" "$TAR_NAME"

# Optionally, you can remove the intermediate tar archive.
rm "$TAR_NAME"


zipinfo "$ZIP_NAME"