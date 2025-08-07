#!/bin/bash
echo "✅ post-install.sh started"
python -m spacy download en_core_web_sm
echo "✅ finished downloading model"
