#!/bin/bash

# To obtain the actual path to repo folder
p=$(dirname $(dirname $(realpath $0)))

# Go to repository
cd $p

# .env path
env_path="${p}/.env"
echo $env_path

# Load the .env file
source "${env_path}"

mkdir -p "${DATA_PATH}"
mkdir -p "${LOGS_PATH}"

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
    echo "Running $script_name"
    $POETRY_PATH run python3 "${scripts_folder}${script_name}.py"
    if [ $? -ne 0 ]; then
        echo "$script_name failed"
        exit 1
    fi
}

# Run fetcher_directus
#run_script "fetcher_directus"

# Run fetcher_botavista
#run_script "fetcher_botavista"

# Run web_page.py
run_script "web_page"
