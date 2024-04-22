import glob
import os
import traceback

from btc_embedded import EPRestApi


def migration_source(ep, model_path, script_path, matlab_version):
    """Generates tests for full coverage on the given model using the
    specified Matlab version, then performs a MIL and SIL simulation
    to record the reference behavior.

    Returns the BTC EmbeddedPlatform Project (*.epp).
    """
    model_path = os.path.abspath(model_path)
    script_path = os.path.abspath(script_path) if script_path else None
    result_dir = os.path.abspath('results')
    epp_file, _ = get_epp_file_by_name(result_dir, model_path)
    
    # Empty BTC EmbeddedPlatform profile (*.epp) + Arch Import
    ep.post('profiles?discardCurrentProfile=true')

    # Import model
    payload = {
        'ecModelFile' : model_path,
        'ecInitScript' : script_path
    } 
    ep.post('architectures/embedded-coder', payload, message="Model Import with Matlab 2020a")
    scopes = ep.get('scopes')
    toplevel_scope_uid = next(scope['uid'] for scope in scopes if scope['architecture'] == 'Simulink')

    # Generate vectors for full coverage
    ep.post('coverage-generation', { 'scopeUid' : toplevel_scope_uid, 'pllString': 'MCDC;RO' }, message="Generating vectors")
    b2b_coverage = ep.get(f"scopes/{toplevel_scope_uid}/coverage-results-b2b")
    print('Coverage ' + "{:.2f}%".format(b2b_coverage['MCDCPropertyCoverage']['handledPercentage']))

    # Simulation
    payload = { 'execConfigNames' : [ 'SL MIL', 'SIL' ] }
    ep.post(f"scopes/{toplevel_scope_uid}/testcase-simulation", payload, message="Reference Simulation on MIL and SIL")

    # Store MIL and SIL executions for comparison
    all_execution_records = ep.get('execution-records')
    payload = { "folderKind": "EXECUTION_RECORD" }
    payload['folderName'] = 'old-mil'
    old_mil_folder = ep.post('folders', payload)
    payload['folderName'] = 'old-sil'
    old_sil_folder = ep.post('folders', payload)

    # MIL
    mil_execution_records_uids = [ er['uid'] for er in all_execution_records if er['executionConfig'] == 'SL MIL']
    ep.put(f"folders/{old_mil_folder['uid']}/execution-records", { 'UIDs' : mil_execution_records_uids })

    # SIL
    sil_execution_records_uids = [ er['uid'] for er in all_execution_records if er['executionConfig'] == 'SIL']
    ep.put(f"folders/{old_sil_folder['uid']}/execution-records", { 'UIDs' : sil_execution_records_uids })

    # Save *.epp and close application
    ep.put('profiles', { 'path': epp_file }, message="Saving profile")

    return epp_file

def migration_target(ep, model_path, script_path, matlab_version):
    """Imports the reference execution records and simulates the same
    vectors on MIL and SIL based on the specified Matlab version. This
    regression test will show any changed behavior compared to the provided 
    reference execution.

    Produces a test report
    """
    model_path = os.path.abspath(model_path)
    script_path = os.path.abspath(script_path) if script_path else None
    result_dir = os.path.abspath('results')
    epp_file, epp_rel_path = get_epp_file_by_name(result_dir, model_path)

    # load BTC EmbeddedPlatform profile (*.epp) -> Update Model
    ep.get(f'profiles/{epp_file}?discardCurrentProfile=true')

    # Arch Update
    payload = {
        'slModelFile' : model_path,
        'slInitScript' : script_path
    } 
    ep.put(f"architectures/model-paths", payload)
    ep.put('architectures', message=f"Updating model & generating code with Matlab {matlab_version}")

    scopes = ep.get('scopes')
    toplevel_scope_uid = next(scope['uid'] for scope in scopes if scope['architecture'] == 'Simulink')
    
    # Import Execution Records
    # create required folders
    payload = { "folderKind": "EXECUTION_RECORD" }
    payload['folderName'] = 'new-mil'
    new_mil_folder = ep.post('folders', payload)
    payload['folderName'] = 'new-sil'
    new_sil_folder = ep.post('folders', payload)

    old_mil_folder = ep.get('folders?name=old-mil')[0]
    old_sil_folder = ep.get('folders?name=old-sil')[0]
    
    # Regression Test
    # -> MIL
    # payload = {}
    # payload['compMode'] = 'SL MIL'
    # payload['compFolderUID'] = new_mil_folder['uid']
    # mil_test = ep.post(f"folders/{old_mil_folder['uid']}/regression-tests", payload, message="Regression Test MIL vs. MIL")
    # # verdictStatus, failed, error, passed, total
    # print(f"Result: {mil_test['verdictStatus']}")

    # -> SIL
    payload = {}
    payload['compMode'] = 'SIL'
    payload['compFolderUID'] = new_sil_folder['uid']
    sil_test = ep.post(f"folders/{old_sil_folder['uid']}/regression-tests", payload, message="Regression Test SIL vs. SIL")
    # verdictStatus, failed, error, passed, total
    print(f"Result: {sil_test['verdictStatus']}")

    ep.post('coverage-generation', { 'scopeUid' : toplevel_scope_uid, 'pllString': 'MCDC;RO' })
    b2b_coverage = ep.get(f"scopes/{toplevel_scope_uid}/coverage-results-b2b")

    # Create project report using "regression-test" template
    # and export project report to a file called '{model_name}-migration-test.html'
    report = ep.post(f"scopes/{toplevel_scope_uid}/project-report?template-name=regression-test", message="Creating test report")
    model_name = os.path.basename(model_path)[:-4].replace('Wrapper_', '')
    ep.post(f"reports/{report['uid']}", { 'exportPath': result_dir, 'newName': f'{model_name}-migration-test' })

    # Save *.epp
    ep.put('profiles', { 'path': epp_file }, message="Saving profile")

    result = {
        'projectName' : f'{model_name}_2020a-vs-2023b',
        'duration' : 0,
        'statementCoverage' : b2b_coverage['StatementPropertyCoverage']['handledPercentage'],
        'mcdcCoverage' : b2b_coverage['MCDCPropertyCoverage']['handledPercentage'],
        'testResult' : sil_test['verdictStatus'],
        'eppPath' : epp_rel_path,
        'reportPath' : f"{model_name}-migration-test.html"
    }
    return result 


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
    ep = EPRestApi()
    ep.put('preferences', [ {'preferenceName' : 'GENERAL_MATLAB_CUSTOM_VERSION', 'preferenceValue' : f'MATLAB R{version} (64-bit)' }, { 'preferenceName' : 'GENERAL_MATLAB_VERSION', 'preferenceValue': 'CUSTOM' } ])
    return ep

def get_epp_file_by_name(result_dir, model_path):
    model_name = os.path.basename(model_path)[:-4].replace('Wrapper_', '')
    return os.path.join(result_dir, model_name + '.epp'), model_name + '.epp'
