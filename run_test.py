from btc_embedded import migration_source, migration_target

# 2020a model files
old_model = 'shc_2020a/Wrapper_seat_heating_control.slx'
old_script = 'shc_2020a/init_Wrapper_seat_heating_control.m'

# 2023b model files
new_model = 'shc_2023b/Wrapper_seat_heating_control.slx'
new_script = 'shc_2023b/init_Wrapper_seat_heating_control.m'

# btc migration test
btc_project = migration_source(old_model, old_script, '2020a')
btc_report = migration_target(new_model, new_script, '2023b', epp_file=btc_project)
