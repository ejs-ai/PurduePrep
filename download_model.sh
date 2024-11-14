#!/bin/bash
# download_model.sh

# Define the model URL (Dropbox URL with `dl=1`)
MODEL_URL="https://www.dropbox.com/scl/fi/wdf2g7qrtjybqc47j4p9y/bert_classifier.pth?rlkey=y11v2o6wwpsj7rkravtt5gzg2&st=zp2y91ga&dl=1"
MODEL_PATH="bert.pth"

# Check if the model file already exists
if [ ! -f "$MODEL_PATH" ]; then
  echo "Downloading model from Dropbox..."
  curl -L -o "$MODEL_PATH" "$MODEL_URL"
  echo "Model downloaded."
else
  echo "Model already exists at $MODEL_PATH"
fi
