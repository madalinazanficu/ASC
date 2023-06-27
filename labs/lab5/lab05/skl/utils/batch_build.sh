#!/bin/bash
singularity exec $CONTAINER_IMAGE  \
make $TASK -f Makefile
