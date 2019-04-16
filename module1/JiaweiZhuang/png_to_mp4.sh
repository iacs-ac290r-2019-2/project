#!/bin/bash

# ffmpeg -framerate 12 -i ./movie/frame_%03d.png -pix_fmt yuv420p movie_temperature.mp4

ffmpeg -framerate 12 -i ./movie_schlieren/frame_sch_%03d.png -pix_fmt yuv420p movie_schlieren.mp4
