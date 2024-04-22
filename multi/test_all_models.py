import glob
import os
import time

from mig2 import (migration_source, migration_target,
                  start_ep_and_configure_matlab)

#
# Matlab 2020a
#
ep = start_ep_and_configure_matlab('2020a')

models_2020a = [os.path.abspath(p) for p in glob.glob('2020a/*.slx')]
for old_model in models_2020a[:2]:
    migration_source(ep, old_model, os.path.abspath('2020a/init.m'), '2020a')

ep.close_application()
time.sleep(5)

#
# Matlab 2023b
#
ep = start_ep_and_configure_matlab('2023b')

models_2023b = [os.path.abspath(p) for p in glob.glob('2023b/*.slx')]
for new_model in models_2023b[:2]: 
    migration_target(ep, old_model, os.path.abspath('2023b/init.m'), '2023b')

ep.close_application()
