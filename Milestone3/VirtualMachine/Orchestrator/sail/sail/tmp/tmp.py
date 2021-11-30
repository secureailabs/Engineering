from ..core import newguid, pushdata, pulldata, submitjob, setparameter, queryresult

def get_tmp_fns():
    fns_dict = {
        "shap_private": "3B3C53AFB1DF415D811E69B32BAB6842",
        "smote": "A9EB0703F1464698B1A173C5A6911127"
    }
    
    return fns_dict


def smote(vmid, oversample, X_data_id, y_data_id, fns):
    jobid = newguid()
    # push string remotely
    inputs = pushdata(vmid, [oversample])
    print(inputs)
    # add test data to inputs
    inputs.append(X_data_id)
    inputs.append(y_data_id)

    setparameter(vmid, jobid, fns["smote"], inputs)
    submitjob(vmid, fns["smote"], jobid)
    pulldata(vmid, jobid, fns["smote"])
    results = queryresult(jobid, fns["smote"])

    return results[0], results[1]


def shap_private(vmid, model, X_data_id, fns):
    jobid = newguid()
    # push string remotely
    inputs = pushdata(vmid, [model])
    print(inputs)
    # add test data to inputs
    inputs.append(X_data_id)

    setparameter(vmid, jobid, fns["shap_private"], inputs)
    submitjob(vmid, fns["shap_private"], jobid)
    pulldata(vmid, jobid, fns["shap_private"])
    results = queryresult(jobid, fns["shap_private"])

    return results[0], results[1], results[2]
