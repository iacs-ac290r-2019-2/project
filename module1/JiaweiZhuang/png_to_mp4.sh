#!/bin/bash

ffmpeg -framerate 12 -i ./movie/frame_%03d.png -pix_fmt yuv420p movie_temperature.mp4
