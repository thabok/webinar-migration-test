import os

from btc_embedded import migration_source, migration_target

# model files to test
old_model = os.path.abspath('shc_2020a/Wrapper_seat_heating_control.slx')
old_script = os.path.abspath('shc_2020a/init_Wrapper_seat_heating_control.m')

new_model = os.path.abspath('shc_2023b/Wrapper_seat_heating_control.slx')
new_script = os.path.abspath('shc_2023b/init_Wrapper_seat_heating_control.m')

# perform migration test
btc_project = migration_source(old_model, old_script, '2020a')
btc_report = migration_target(btc_project, new_model, new_script, '2023b')
