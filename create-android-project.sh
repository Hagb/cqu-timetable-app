#!/bin/sh
pip install briefcase
PYTHONDONTWRITEBYTECODE=1 SKIP_CYTHON=1 briefcase create android
for APP_PATH in android/gradle/*/app/; do
	break
done
# reduce size
find "${APP_PATH}"/src/main/assets/python/app_packages/pytz/zoneinfo/ -type f ! -name Shanghai -exec rm '{}' \;
find "${APP_PATH}"/src/main/assets/python/app_packages/pytz/zoneinfo/* -depth -type d ! -name Asia -exec rmdir '{}' \;
find "${APP_PATH}"/src/main/assets/python -depth -name __pycache__ -exec rm -r '{}' \;
for type in sqlite3 lzma ssl crypto; do
	rm "${APP_PATH}"/libs/*/lib${type}.so
done

for STRIP in ~/.briefcase/tools/android_sdk/ndk/*/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-strip; do
	break
done
for zipfile in "${APP_PATH}"/src/main/assets/stdlib/*.zip; do
	platform=$(printf %s "$zipfile" | sed -E 's|.*/pythonhome\.[0-9a-zA-Z]+\.([^\.]+)\.zip|\1|')
	unzipdir=${APP_PATH}/src/main/assets/stdlib/
	unzip -q "$zipfile" -d "$unzipdir"
	"${STRIP}" "$unzipdir"/lib/python*/lib-dynload/*.so
	./strip_doc_comments.py "$unzipdir"/lib/
	rm "$zipfile"
	( cd "$unzipdir" ; zip -qmr $platform.zip lib ; mv $platform.zip pythonhome."$(sha256sum $platform.zip | cut -d' ' -f1)".$platform.zip; )
done
