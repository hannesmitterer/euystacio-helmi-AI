#!/bin/bash
# Euystacio fail-safe deployment script
# Motto: in consensus sacralis omnibus est

cd ~/euystacio \
  && git pull origin main \
  && pip install -r requirements.txt \
  && python app.py