FROM lscr.io/linuxserver/blender:latest

ADD ./blender /config/bampe-visualizations

RUN ls -lrth /config/bampe-visualizations/*
