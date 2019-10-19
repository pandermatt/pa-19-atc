mkdir converted
for file in *.wav; do ffmpeg -i "$file" -ar 16000 "converted/$file"; done