# Iteration 1 Results Discussion



## Projected Outcomes 
- Implement horizontally Federated Learning using SAIL platform
  - Create prediction csv files which will be consumed by the NGOs
  - Predictions made must be explainable with Shapley values
- Feature Engineering 
  - Generate output which will inform future iterations of feature engineering code

## Format of Experiment

In this experiment we have 3 parties. Two Data Owners and a Researcher. The Data Owners upload their unique but structurally similar datasets to the SAIL platform using the remote data connector. The remote data connector uploads data to a Secure Virtual Machine (VM) when a contract is provisioned so the Researcher may execute remote commands as the orchestrator.

We perform remote learning in four scenarios:

- We execute remote learning on only the SCL dataset
- We execute remote learning on only the GFR dataset 
- We execute federated learning on both datasets GFR and SCL

### Hypotheses

- Using the SimFL algorithm, we can produce a model that exceeds the performance of a baseline random classifier.
- Training the SimFL algorithm on multiple datasets can produce a model which exceeds the performance of the same model trained on individual datasets.
- Training a SimFL classifier on multiple datasets will give comparable results to training a normal decision boost tree. 

### Constraints

- The Researcher must not access the NGO data in plaintext in the performance of the experiment.
- The Researcher must only compute on data through the use of code contained in safe functions.
- The Researcher may only consume the outputs of safe functions
- The outputs of safe functions must not compromise the privacy of the researcher

### The Algorithm: SimFL
In this iteration we implement a horizontal federated learning experiment using the SimFL algorithmm as outlined in [Practical Federated Gradient Boosting Decision Trees](https://arxiv.org/pdf/1911.04206.pdf). SimFL implements a version of gradient boosting decision trees where each party boosts a number of trees by exploiting shared similarity information based on [Locality Sensitive Hashing (LSH)](https://www.researchgate.net/publication/2634460_Similarity_Search_in_High_Dimensions_via_Hashing). The SimFl algorithm has two distinct phases; the preprocessing phase and the training phase.

<p align="center">
  <img src="images\SimFL_algo.PNG" height=300>
</p>

#### Preprocessing SimFL
 During preprocessing, parties aim to find the identities of similar instances to their own that are held by other parties. In order to do this without exposing the raw data to other parties, instances are converted into hashes using LSH. The ideas is that if instances are similar, the LSH will be identical. Each party constructs a hash table and maps these hashes to instance identities using ```AllReduce```. Hash tables are broadcast by each party to the other parties who will then construct a similarity matrix. This step only needs to be run once per data federation per experiment.

#### Training SimFL
With the similarity matrix collaboratively produced by each party, each party trains their trees sequentially. When party $P_m$ is training their tree, only local instances $I_m$ are used to train. However, given that the hash of element $I_m$ collides with an instance $I_n$ owned y $M_n$, a weighted gradient is applied to $I_n$ by $M_n$. For each collision that an instances has, a greater gradient is applied to that instance. SimFL implements gradient boosting with this weighted gradient effect for local models.

### The Data: NGO Federation Customer Churn

The datasets used to train our model were provided by a federation of two NGOs who are referred to as SCL and GFR. These datasets are composed of three tables which are preprocessed into a time series format where each instance represents whether a customer has churned. Instances are indexed by the unique customer GUID and the data at which this instance is measuring. 

The target of our prediction is a binary class indicating whether a customer has churned in the last three months. The target class is extremely imbalanced with 78 negative instances to every 1 positive instance in the GFR dataset and 61 to 1 in the case of SCL. There are around 80 features to the data. By ethical and legal requirement, specifics of the dataset remain unknown to the researchers.

For purposes of this experiment the data has been split into 3 chunks:

- The `training set`, used to train SimFL
- The `validation set`, used to understand model performance
- The `test set`, used to generate predictions and Shapley values on most recent cases to be consumed by NGOs in the federation

### Remote Execution Platform: SAIL

The SAIL platform consists of 6 base components. These are utilized to create a secure environment which facilitates federated learning. 

#### The Dataset Specifiction Tool (DST)
The DST is used by Data Owners to specify their data in the appropriate format to be consumed by the rest of the infrastructure.

#### The Remote Data Connector (RDC)
The RDC uploads a given dataset or group of datasets associated with a digital contract to a remote secure execution environment.

#### The Secure VM (SVM)
The SVM is a VM which is initialized once a contract is provisioned. The SVM receives a dataset from the RDC and executes Safe Functions supplied by the Orchestrator. Once execution is complete, the SVM is destroyed along with all data contents. The SVM can only execute SAIL minted Safe Functions and has strong logging mechanisms for audit.

#### Safe Functions (SFs)
Safe Functions are the core component of the remote execution infrastructure. These are immutable pieces of code which have been defined, tested and hardened against security leakage. The purpose of safe functions is to facilitate contextually appropriate privacy-preserving information flows between the secret assets on the SVM and the Orchestrator.

#### The Orchestrator
The Orchestrator is a python library designed to used inside a jupyter notebook environment. This can also be executed as a pure python script. The Orchestrator connects to the SVM and supplies SFs in order to perform some computation flow on the data and return the result.

#### The SAIL WebAPI
The WebAPI allows data owners to accept contract requests and for researchers to discover data, propose contracts for this data and provision SVMs to operate on it.

## Results

<p align="center">
<table>
<tr><th>SCL Results</th><th>GFR Results</th></tr>
<tr><td>

| Model             | Avg. Precision |
| ----------------- | :------------: |
| Baseline          |     0.015      |
| Single Node SimFL |     0.065      |
| Federated SimFL   |     0.058      |
| Local XGBoost     |      0.07      |


</td><td>

| Model             | Avg. Precision |
| ----------------- | :------------: |
| Baseline          |     0.011      |
| Single Node SimFL |     0.020      |
| Federated SimFL   |     0.017      |
| Local XGBoost     |      0.03      |

</td></tr> </table>
</p>

<p align="center">
  <table>
<tr><th>SCL Single Node SimFL</th><th>SCL Federated SimFL</th><th>SCL Local XGBoost</th></tr>
<tr><td>
    <img src="images\SCL_only_AUC.png"> 
</td><td>
    <img src="images\SCL_FED_AUC.png" >
</td><td>
    <img src="images\SCL_KPMG_AUC.png">
</td></tr> </table>
</p>

<p align="center">
  <table>
<tr><th>GFR Single Node SimFL</th><th>GFR Federated SimFL</th><th>GFR Local XGBoost</th></tr>
<tr><td>
    <img src="images\GFR_only_AUC.png"> 
</td><td>
    <img src="images\GFR_FED_AUC.png">
</td><td>
    <img src="images\GFR_KPMG_AUC.png">
</td></tr> </table>
</p>

## Discussion

The baseline model performance was exceeded by all classifiers. This demonstrates that models were able to develop some degree of skill after learning the training sets. However, the extent of this differs greatly between the two datasets. The model with greatest performance achieves average precision 0.07 with SCL and GFR at 0.03. This is a substantive difference. 

It's unclear whether this disparity can explain the poor performance of the federated classifier. It was demonstrated that in the case of the GFR and SCL, federated training did not produce results which exceeded either model trained individually. The federated classifier was unable to match the average precision of either the locally trained xgboost model or the SimFL model trained on the individual datasets. Data drift could account for this lack of coherence. 

The  SimFL models trained on individual sets were outperformed by the local XGBoost model trained under ideal conditions. A small loss in performance is to be expected with potential information lost during the LSH phase of preprocessing. 

 In all cases the predictive performance of classifiers was not ideal and it is unclear whether every dataset is suitable for predicting customer churn. The SCL dataset shows much greater predictive potential than GFR. This could potentially be balanced out by adding more NGOs to the federation.

It was clear that in this case the models trained on independent nodes performed best. If we were to choose a different algorithm to perform federated training/ predicition, [PATE](https://openreview.net/pdf?id=rkZB1XbRZ) style ensemble classifier could be approprite.

However, we know the SimFL algorithm works well in cases where datasets are uniformally distributed. Another promising route would be to perform extended feature exploration/ distribution analysis to diagnose issues of dissimilarity between datasets. 

## Known Issues

### Algorithm/ Infrastructure Issues

While implementing the SimFL algorithm on the SAIL infrastructure, we ran into a number of issues. These were largely discovered and fixed during the course of Iteration 1. However, issues still persist:

- Memory Consumption
- Complications in SimFL Parallelization 

While consistent with centralized learning, the SimFL implementation was found to be quite inefficient when processing larger datasets. Intensive memory usage makes this build unstable and causes complications in state management in our infrastructure. SAIL will address this memory consumption issue in the next iteration. 

The SimFL algorithm is running on distributed infrastructure and this adds a layer of complexity. We need to expand upon features on the orchestrator side to negotiate this training sequence with the remote VMs in parallel. A lack of parallelization makes this slow to run to completion. Slow processing speeds severely inhibit our ability to run hyperparameter optimization over a large number of iterations. This is an issue which will be resolved by SAIL in future iterations.


### Data Issues
There are a number of points where we believe we could improve the model performance by enhancing the feature engineering sections.

#### Improved Data Imputation
The first is that there are a large number of NaN values in the dataset. NaN values cannot be hashed properly by SimFL and so we change all NaN values to 0 by default in the preprocessing script. However, we believe it would yield better results if these data points were to be imputed with something meaningful for that column; the mean value for example.

#### Dataset Incongruence
The predictive performance of the federated model can partially be explained by structural dissimilarities between datasets SCL and GFR. Further investigation should go into this by the data owner federation. We were able to pick up on this potential through disparities found between the SHAP bee swarm plots (See below). While differences in SHAP output can be explained through covariance between features in specific examples, it can also mean that the structure learned by the model is incongruent. We've attached shap output for each model trained individually. However, our ability to accurately diagnose and fix is limited/ time expensive due to privacy constraints.

<p align='center'>
    <img src="images\GFR_SHAP_Beeswarm.png" height=400>
    <img src="images\SCL_SHAP_Beeswarm.png" height=400>

#### Potential Date Formatting Logic Error
There is a potential logic error in the way that date is where churn is allocated to dates. This compares year then month. However, it is unclear whether this compensates for months between November and February where there will be no wrap around for time periods between months 10 and 02 of the following year.

```
# Churned within three months
agg_df["is_churned_within3m"] = np.where((agg_df['CancelDate_y_min'].dt.year <= agg_df["PaymentDate_"].dt.year) &
                                   (agg_df['CancelDate_y_min'].dt.month <= agg_df["PaymentDate_"].dt.month+3), True, False)
```

#### Covid Data Drift
A time series model may be frustrated by a change in consumer behavior over the last year. Covid has likely caused new competition between NGOs which may skew instances gathered more recently. This is likely compounded by the economic impact of the virus. We believe this may be a source of data drift. We can avoid this by trimming a large amount of the old data. 

#### Feature Reduction
Currently we run the model over 80 features. However, according to our SHAP plots, a large number of these are not useful. We would recommend making a cut-off to just the features included in the diagram below. Unnecessary features create unnecessary noise for the model to deal with. We recommend you choose only a minority of these features. Below they are listed in order of importance.

<p align='center'>
    <img src="images\too_many_features.png" style="transform:rotate(270deg);" height=600>
<p>

#### Postcode Feature Generation
We see that postcode is a feature in your dataset. We can combine this with government statistics on postcodes to generate features relating to the customer demographic. For example, in Scotland we have the [Scottish Index of Multiple Deprivation (SIMD)](https://www.gov.scot/collections/scottish-index-of-multiple-deprivation-2020/). This is publicly maintained data which associates postcodes into quintile, decile and vigntile ranks. This can be an informative feature relating to customer demographic. This strategy could be applicable in the feature engineering here. 

#### NGO Indicator Feature
In order to stem potential incongruence between datasets, we recommend a categorical feature to be added to each instance which indicates which dataset it belongs to.


## Conclusion
While the SimFL learning model could be train in the distributed environment and exceed the performance of the baseline, the extent to which this was exceeded is poor. In this case the model trained on the federated sets was the least performant. In this iteration, we have been unsuccessful in meeting this requirement of the study and we should consider how to proceed with Iteration 2.

### Proposed Goals for Iteration 2

- Improve upon SIMFL computational performance
- Improve upon feature engineering of the GFR and SCL datasets
- Establish priorities for feature engineering

## Deliverable Checklist
- ```Fed_NGOs``` 
  - ```orchestrator_federated_clean.ipynb``` containing results for the single training example
  - ```predictions_federated_shap_GFR_test.csv```, containing predictions and shap values corresponding to the predictions of the test dataset of GFR, to be consumed by GFR. Pertains to SAIL optimised notebook.
  - ```predictions_federated_shap_SCL_test.csv```, containing predictions and shap values corresponding to the predictions of the test dataset of GFR, to be consumed by SCL. Pertains to SAIL optimised notebook.
- ```SCL_only```
  - ```orchestrator_Federated_clean.ipynb```, contains results from training SimFL on only SCL.
  - ```predictions_shap_SCL_test.csv```, contains predictions and shap values corresponding to SCL test.
- ```GFR_only```
  - ```orchestrator_Federated_clean.ipynb```, contains results from training SimFL on only SCL.
  - ```predictions_shap_GFR_test.csv```, contains predictions and shap values corresponding to SCL test.
