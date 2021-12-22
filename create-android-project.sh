#!/bin/bash
pip install briefcase
PYTHONDONTWRITEBYTECODE=1 SKIP_CYTHON=1 briefcase create android
# reduce size
find android/gradle/*/app/src/main/assets/python/app_packages/pytz/zoneinfo/ -type f ! -name Shanghai -exec rm '{}' \;
find android/gradle/*/app/src/main/assets/python/app_packages/pytz/zoneinfo/* -depth -type d ! -name Asia -exec rmdir '{}' \;
find android/gradle/*/app/src/main/assets/python -depth -name __pycache__ -exec rm -r '{}' \;
rm android/gradle/*/app/libs/*/lib{sqlite3,lzma,ssl,crypto}.so
