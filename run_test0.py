import os

from mig0 import migration_source, migration_target

source_model = os.path.abspath('shc_2020a/Wrapper_seat_heating_control.slx')
source_script = os.path.abspath('shc_2020a/init_Wrapper_seat_heating_control.m')

target_model = os.path.abspath('shc_2023b/Wrapper_seat_heating_control.slx')
target_script = os.path.abspath('shc_2023b/init_Wrapper_seat_heating_control.m')

# perform migration test
mil, sil = migration_source(source_model, source_script, '2020a')
btc_report = migration_target(target_model, target_script, '2023b', mil, sil)
