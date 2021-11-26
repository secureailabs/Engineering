import sail.core
import json
import time

def main():
    sail.core.login("lbart@igr.com", "SailPassword@123", "AuthCode")

    print("Getting list of safe functions")
    safe_fns = sail.core.getlistofsafefunctions()

    print(safe_fns.split(","))

    print("Information for safe_fn")
    safe_fn_guid = safe_fns.split(",")[1].split(":")[0]
    print("Safe fn guid",safe_fn_guid)
    safe_fn_info = json.loads(sail.core.GetSafeFunctionInformation(safe_fn_guid))
    print("Number of input parameters {}".format(len(safe_fn_info["InputParameters"].keys())))
    print(safe_fn_info["InputParameters"])

    job_id = sail.core.RunJob(safe_fn_guid)

    print("Initialized job {}".format(job_id))

    print("Job status: {}".format(sail.core.GetJobStatus(job_id)))

    param_ids = {}
    pushed_data = sail.core.PushData("Some pushed test data as a string")
    print("Pushed data",pushed_data)
    # Dummy up some data
    for input_param in safe_fn_info["InputParameters"]:
        param_uuid = safe_fn_info["InputParameters"][input_param]['Uuid']
        print("Setting data for param", param_uuid)
        param_ids[input_param] = sail.core.SetParameter(job_id, param_uuid, pushed_data)
        print("Param id is",param_ids[input_param])
        print("Job status is",sail.core.GetJobStatus(job_id))

    print("Parameters filled in for Safe FN:",safe_fn_info["Description"])

    dc_list = sail.core.getlistofdigitalcontracts()

    print("Digital contracts",dc_list)

    dc_provision = dc_list.split(",")[0].split(":")[0]
    dc_provision2 = dc_list.split(",")[1].split(":")[0]
    print("DC to provision", dc_provision)

    sail.core.ProvisionDigitalContract(dc_provision,"FAKE_GUID")
    sail.core.ProvisionDigitalContract(dc_provision2,"FAKE_GUID")

    print("I have finished")

    wait_return = sail.core.WaitForDigitalContractsToBeProvisioned()

    print(wait_return)

if __name__ == "__main__":
    main()