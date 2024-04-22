import glob
import os
import shutil
import time

from btc_embedded import create_test_report_summary
from mig2 import (migration_source, migration_target,
                  start_ep_and_configure_matlab)

#
# Matlab 2020a
#
# shutil.rmtree('results')
# ep = start_ep_and_configure_matlab('2020a')

# models_2020a = [os.path.abspath(p) for p in glob.glob('2020a/*.slx')]
# for old_model in models_2020a[:2]:
#     migration_source(ep, old_model, os.path.abspath('2020a/init.m'), '2020a')

# ep.close_application()

#
# Matlab 2023b
#
ep = start_ep_and_configure_matlab('2023b')

results = []
models_2023b = [os.path.abspath(p) for p in glob.glob('2023b/*.slx')]
for new_model in models_2023b[:2]: 
    result = migration_target(ep, new_model, os.path.abspath('2023b/init.m'), '2023b')
    results.append(result)

ep.close_application()

create_test_report_summary(results, 'BTC Migration Test Suite', 'BTCMigrationTestSuite.html', 'results')