#!/bin/bash

# conda activate ac290  # do this outside of the script

for k in 0.5 1 2 5 10; do
    mkdir -p movie_schlieren_k${k}
    python make_schlieren.py ${k}

    ffmpeg -framerate 12 -i ./movie_schlieren_k${k}/frame_%03d.png -pix_fmt yuv420p movie_schlieren_k${k}.mp4
done

