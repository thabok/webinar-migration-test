import glob
import os
import traceback

from btc_embedded import EPRestApi


def migration_source(model_path, script_path, matlab_version):
    """Generates tests for full coverage on the given model using the
    specified Matlab version, then performs a MIL and SIL simulation
    to record the reference behavior.

    Returns a list of MIL execution records and a list of SIL execution records.
    """
    model_path = os.path.abspath(model_path)
    script_path = os.path.abspath(script_path) if script_path else None
    work_dir = os.path.dirname(model_path)
    epp_file_source = model_path.replace('.slx', '_source.epp')
    
    ep = start_ep_and_configure_matlab(matlab_version)

    # Empty BTC EmbeddedPlatform profile (*.epp) + Arch Import
    ep.post('profiles?discardCurrentProfile=true')

    # Import model
    payload = {
        'ecModelFile' : model_path,
        'ecInitScript' : script_path
    } 
    ep.post('architectures/embedded-coder', payload, message="Model Import")
    scopes = ep.get('scopes')
    toplevel_scope_uid = next(scope['uid'] for scope in scopes if scope['architecture'] == 'Simulink')

    # Generate vectors for full coverage
    ep.post('coverage-generation', { 'scopeUid' : toplevel_scope_uid, 'pllString': 'MCDC' }, message="Generating vectors")
    b2b_coverage = ep.get(f"scopes/{toplevel_scope_uid}/coverage-results-b2b")
    print('Coverage ' + str(b2b_coverage['MCDCPropertyCoverage']['handledPercentage']))

    # Simulation
    payload = { 'execConfigNames' : [ 'SL MIL', 'SIL' ] }
    ep.post(f"scopes/{toplevel_scope_uid}/testcase-simulation", payload, message="Simulating on MIL and SIL")

    # Execution Record Export
    all_execution_records = ep.get('execution-records')

    # MIL
    mil_execution_records_uids = [ er['uid'] for er in all_execution_records if er['executionConfig'] == 'SL MIL']
    mil_dir = os.path.join(work_dir, 'execution_records', 'MIL')
    payload = { 'UIDs' : mil_execution_records_uids, 'exportDirectory': mil_dir, 'exportFormat' : 'MDF' }
    ep.post('execution-records-export', payload)

    # SIL
    sil_execution_records_uids = [ er['uid'] for er in all_execution_records if er['executionConfig'] == 'SIL']
    sil_dir = os.path.join(work_dir, 'execution_records', 'SIL')
    payload = { 'UIDs' : sil_execution_records_uids, 'exportDirectory': sil_dir, 'exportFormat' : 'MDF' }
    ep.post('execution-records-export', payload)

    # Save *.epp and close application
    ep.put('profiles', { 'path': epp_file_source }, message="Saving profile")

    execution_records_root_dir = os.path.dirname(mil_dir)
    return get_existing_references(execution_records_root_dir)


def migration_target(model_path, script_path, matlab_version, mil_executions, sil_executions):
    """Imports the reference execution records and simulates the same
    vectors on MIL and SIL based on the specified Matlab version. This
    regression test will show any changed behavior compared to the provided 
    reference execution.

    Produces a test report
    """
    model_path = os.path.abspath(model_path)
    script_path = os.path.abspath(script_path) if script_path else None
    work_dir = os.path.dirname(model_path)
    epp_file_target = model_path.replace('.slx', '_target.epp')

    ep = start_ep_and_configure_matlab(matlab_version)

    # Empty BTC EmbeddedPlatform profile (*.epp) + Arch Import
    ep.post('profiles?discardCurrentProfile=true')

    # Arch Import
    payload = {
        'ecModelFile' : model_path,
        'ecInitScript' : script_path
    } 
    ep.post('architectures/embedded-coder', payload, message="Model Import")
    scopes = ep.get('scopes')
    toplevel_scope_uid = next(scope['uid'] for scope in scopes if scope['architecture'] == 'Simulink')

    scopes = ep.get('scopes')
    toplevel_scope_uid = next(scope['uid'] for scope in scopes if scope['architecture'] == 'Simulink')
    
    # Import Execution Records
    # create required folders
    payload = { "folderKind": "EXECUTION_RECORD" }
    payload['folderName'] = 'old-mil'
    old_mil_folder = ep.post('folders', payload)
    payload['folderName'] = 'new-mil'
    new_mil_folder = ep.post('folders', payload)
    payload['folderName'] = 'old-sil'
    old_sil_folder = ep.post('folders', payload)
    payload['folderName'] = 'new-sil'
    new_sil_folder = ep.post('folders', payload)
    # import mil executions
    payload = {} 
    payload['paths'] = mil_executions
    payload['kind'] = 'SL MIL'
    payload['folderUID'] = old_mil_folder['uid']
    ep.post('execution-records', payload)
    # import sil executions
    payload = {} 
    payload['paths'] = sil_executions
    payload['kind'] = 'SIL'
    payload['folderUID'] = old_sil_folder['uid']
    ep.post('execution-records', payload)
    
    # Regression Test
    # -> MIL
    payload = {}
    payload['compMode'] = 'SL MIL'
    payload['compFolderUID'] = new_mil_folder['uid']
    mil_test = ep.post(f"folders/{old_mil_folder['uid']}/regression-tests", payload, message="MIL vs. MIL")
    # verdictStatus, failed, error, passed, total
    print(mil_test['verdictStatus'])
    # export ERs
    new_records_mil = ep.get(f"folders/{new_mil_folder['uid']}/execution-records")
    payload = {
        'UIDs' : [er['uid'] for er in new_records_mil],
        'exportDirectory' : os.path.abspath(os.path.join(work_dir, 'new_executions', 'MIL')),
        'exportFormat' : 'MDF'
    }
    ep.post('execution-records-export', payload)

    # -> SIL
    payload = {}
    payload['compMode'] = 'SIL'
    payload['compFolderUID'] = new_sil_folder['uid']
    sil_test = ep.post(f"folders/{old_sil_folder['uid']}/regression-tests", payload, message="SIL vs. SIL")
    # verdictStatus, failed, error, passed, total
    print(sil_test['verdictStatus'])
    # export ERs
    new_records_sil = ep.get(f"folders/{new_sil_folder['uid']}/execution-records")
    payload = {
        'UIDs' : [er['uid'] for er in new_records_sil],
        'exportDirectory' : os.path.abspath(os.path.join(work_dir, 'new_executions', 'SIL')),
        'exportFormat' : 'MDF'
    }
    ep.post('execution-records-export', payload)

    # Create project report using "regression-test" template
    # and export project report to a file called '{model_name}-migration-test.html'
    report = ep.post(f"scopes/{toplevel_scope_uid}/project-report?template-name=regression-test", message="Creating test report")
    model_name = os.path.basename(model_path)[:-4]
    ep.post(f"reports/{report['uid']}", { 'exportPath': work_dir, 'newName': f'{model_name}-migration-test' })

    # Save *.epp
    ep.put('profiles', { 'path': epp_file_target }, message="Saving profile")

def get_existing_references(execution_record_folder):
    mil_executions = [os.path.abspath(p) for p in glob.glob(f"{execution_record_folder}/MIL/*.mdf")]
    sil_executions = [os.path.abspath(p) for p in glob.glob(f"{execution_record_folder}/SIL/*.mdf")]
    return mil_executions, sil_executions

def handle_error(ep, epp_file, step_result):
    step_result['status'] = 'ERROR'
    step_result['message'] = traceback.format_exc()
    ep.put('profiles', { 'path': epp_file }, message="Saving profile")
    print(step_result['message'])

def start_ep_and_configure_matlab(version):
    ml_port_map = {
        '2020a' : 1337,
        '2023b' : 1338
    }
    ep = EPRestApi(port=ml_port_map[version])
    ep.put('preferences', [ {'preferenceName' : 'GENERAL_MATLAB_CUSTOM_VERSION', 'preferenceValue' : f'MATLAB R{version} (64-bit)' }, { 'preferenceName' : 'GENERAL_MATLAB_VERSION', 'preferenceValue': 'CUSTOM' } ])
    return ep