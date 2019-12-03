#!/bin/bash
# compress all *.jpg files in the current directory
# and place them in ./compressed directory
# with the same modification date as original files.

jpegoptim --size=75k /var/www/CodeIgniter/images/*.jpg