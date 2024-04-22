import os

from mig1 import migration_source, migration_target

source_model = os.path.abspath('shc_2020a/Wrapper_seat_heating_control.slx')
source_script = os.path.abspath('shc_2020a/init_Wrapper_seat_heating_control.m')

target_model = os.path.abspath('shc_2023b/Wrapper_seat_heating_control.slx')
target_script = os.path.abspath('shc_2023b/init_Wrapper_seat_heating_control.m')

# perform migration test
print("""
###############################################################
#                                                             #
#   BTC MIGRATION TEST: ML 2020a <--> ML 2023b                #
#                                                             #
#   (1) Recording reference behavior on ML 2020a              #
#                                                             #
###############################################################
""")
btc_project = migration_source(source_model, source_script, '2020a')

print("""
###############################################################
#                                                             #
#   BTC MIGRATION TEST: ML 2020a <--> ML 2023b                #
#                                                             #
#   (2) Comparing reference behavior with ML 2023b behavior   #
#                                                             #
###############################################################
""")
btc_report = migration_target(btc_project, target_model, target_script, '2023b')
