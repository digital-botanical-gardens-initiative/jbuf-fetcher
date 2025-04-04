#!/bin/bash

# To obtain the actual path to repo folder
p=$(dirname $(dirname $(realpath $0)))

# .env path
env_path="${p}/.env"

# Load the .env file
source "${env_path}"

# Go to repository
cd $p

# Update repository
git pull origin main

# Update python dependencies
eval "$POETRY_PATH install"

# Create folders
mkdir -p $DATA_PATH
mkdir -p $HTML_PATH
mkdir -p $LOGS_PATH

cp "./jbuf_fetcher/styles.css" "${HTML_PATH}/styles.css"
cp -r "./images" "${HTML_PATH}"

# Clean logs folder if the used space is greater than 100MB
SIZE_LIMIT_MB=100

# Get the folder size in MB
FOLDER_SIZE_MB=$(du -sm "$LOGS_PATH" | awk '{print $1}')

# Check if the folder size exceeds the limit
if [ "$FOLDER_SIZE_MB" -gt "$SIZE_LIMIT_MB" ]; then
    echo "Folder size ($FOLDER_SIZE_MB MB) exceeds the limit ($SIZE_LIMIT_MB MB). Deleting contents..."

    # Delete all contents of the folder
    rm -rf "${LOGS_PATH}/*"

    echo "Contents of the folder have been deleted."
fi

# Get scripts folder
scripts_folder="${p}/jbuf_fetcher/"

# Run a script and check its return code
run_script() {
    script_name=$1
    # Redirect all output to the log file
    exec &>> "$LOGS_PATH/$script_name.log"
    echo "Running $script_name $(date)"
    $POETRY_PATH run python3 "${scripts_folder}${script_name}.py"
    if [ $? -ne 0 ]; then
        echo "$script_name failed"
        exit 1
    fi
}

# Get current minute, hour, and day
MINUTE=$(date +\%M)
HOUR=$(date +\%H)
DAY=$(date +\%d)

echo "$MINUTE $HOUR $DAY"

# Run fetcher_directus and taxo_resolver every 2 hours at 30
if [[ "$MINUTE" == "30" && $((HOUR % 2)) -eq 0 ]]; then
    run_script "directus_fetcher"
    run_script "botavista_fetcher"
    run_script "taxo_resolver"
    run_script "data_processing"
fi

# Update html
run_script "html_generator"

# Transfer the html and CSS file to the server
eval "$RSYNC_COMMAND"
