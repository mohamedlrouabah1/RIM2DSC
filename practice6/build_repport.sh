#!/usr/bin/bash
source .env

ZIP_NAME="rendus/practice""$NUM_TP""_""$GROUP_NAME"".zip"
FILES_TO_EXCLUDE=(
    "**/__pycache__/*"
    "practice$NUM_TP/*.pdf"
    "**/.*pytest_cache/v/cache/*"
    "**/.*pytest_cache/v/cache/"
    "**/.*pytest_cache/v/"
    "**/.*pytest_cache/*"
    "**/.*pytest_cache/.gitignore"
    "**/.*pytest_cache/"
    "**/build/**/"
    "**/build/"
    "**/information_retrieval.egg-info/*"
    "**/information_retrieval.egg-info/"
)

EXCLUDED_FILES="-x "
for file in "${FILES_TO_EXCLUDE[@]}"
do
    EXCLUDED_FILES+="$file "
    echo -e "excluded file: $file\n"
done

echo "EXCLUDED_FILES :" $EXCLUDED_FILES


# move the run file outside result folder
mv "practice$NUM_TP"/results/MohammedWilliam*.txt "practice$NUM_TP"


zip -9 "$ZIP_NAME" -r "practice$NUM_TP" $EXCLUDED_FILES

zipinfo "$ZIP_NAME"

# move the run file back to result folder
mv "practice$NUM_TP"/MohammedWilliam*.txt "practice$NUM_TP/results/"