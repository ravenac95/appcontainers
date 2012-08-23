"""
appcontainers.constants
~~~~~~~~~~~~~~~~~~~~~~~

Constants for appcontainers
"""
import os


OVERLAYS_DIR = 'overlays'
OVERLAYS_RAW_DIR = 'raw'
OVERLAYS_IMAGE_DIR = 'image'
OVERLAYS_TMP_DIR = 'tmp'

IMAGES_DIR = 'images'

IMAGES_CONTAINER_DIR = os.path.join(IMAGES_DIR, 'container')
IMAGES_LIB_DIR = os.path.join(IMAGES_DIR, 'lib')
BASE_IMAGES_DIR = os.path.join(IMAGES_DIR, 'base')

IMAGES_USER_DIR = 'container'

SKELETONS_DIR = 'skeletons'

IMAGE_FILE_EXTENSION = 'aimg'

DATABASE_NAME = 'db/state.zdb'
