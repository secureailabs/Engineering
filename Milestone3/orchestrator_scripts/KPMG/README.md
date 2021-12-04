# Iteration 1 Results Discussion



## Projected Outcomes 
- Implement horizontally Federated learning using SAIL platform
  - Create prediction csv files which will be consumed by the NGOs
  - Predictions made must be explainable with Shapley values
  - implement hyperparameter optimization for federated model training
- Feature Engineering 
  - Generate output which will inform future iterations of feature engineering code

## Format of Experiment

In this experiment we have 3 parties. Two Data Owners and a Researcher. The Data Owners upload their unique but structurally similar datasets to the SAIL platform using the remote data connector. The remote data connector uploads data to a Secure Virtual Machine (VM) when a contract is provisioned so the Researcher may execute remote commands as the orchestrator.

We perform remote learning in four scenarios:

- We execute remote learning on only the SCL dataset
- We execute remote learning on only the GFR dataset 
- We compute federated training on both datasets GFR and SCL with hyperparameter optimisation

### Hypotheses

- Federated learning using SimFL can produce a model that exceeds the performance of a baseline random classifier.
- Federated learning using SimFL can produce a model that exceeds the performance of models trained individually.
- The features contained in the GFR and SCL datasets contain appropriate information to predict customer churn.
- predictions made by a federated algorithm will provide more robust predictions for the NGOs than models trained individually.
- The SAIL platform is capable of performing remote data science on the datasets produced by GFR and SCL.

### Constraints

- The Researcher must not access the NGO data in plaintext in the performance of the experiment.
- The Researcher must only compute on data through the use of code contained in safe functions.
- The Researcher may only consume the outputs of safe functions
- The outputs of safe functions must not compromise the privacy of the researcher

### Remote Execution Platform: SAIL

The SAIL platform consists of 6 base components. These are utilised to create a secure environment which facilitates federated learning. 

#### The Dataset Specifiction Tool (DST)
The DST is used by Data Owners to specify their data in the appropriate format to be consumed by the rest of the infrastructure.

#### The Remote Data Connector (RDC)
The RDC uploads a given dataset or group of datasets associated with a digital contract to a remote secure execution environment.

#### The Trusted Execution Environment (TEE)
The TEE is a VM which is initialised once a contract is provisioned. The TEE receives a dataset from the RDC and executes Safe Functions supplied by the Orchestrator. Once execution is complete, the TEE is destroyed along with all data contents. The TEE can only execute SAIL minted Safe Functions and has strong logging mechanisms for audit.

#### Safe Functions (SFs)
Safe Functions are the core component of the remote execution infrastructure. These are immutable pieces of code which have been defined, tested and hardened against security leakage. The purpose of safe functions is to facilitate contextually appropriate privacy-preserving information flows between the secret assets on the TEE and the Orchestrator.

#### The Orchestrator
The Orchestrator is a python library designed to used inside a jupyter notebook environment. This can also be executed as a pure python script. The Orchestrator connects to the TEE and supplies SFs in order to perform some computation flow on the data and return the result.

#### The SAIL WebAPI
The WebAPI allows data owners to accept contract requests and for researchers to discover data, propose contracts for this data and provision TEEs to operate on it.

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

The datasets used to train our model were provided by a federation set of two NGOs who will be referred to as SCL and GFR. These datasets are composed of a set of three tables which are preprocessed into a time series format where each instance represents whether a customer has churned or not at a given date. Instances are indexed by the unique customer GUID and the data at which this instance is measuring. 

The target of our prediction is a binary class indicating whether a customer has churned in the last three months. The target class is extremely imbalanced with 78 negative instances to every 1 positive instance in the GFR dataset and 61 to 1 in the case of SCL. There are around 80 features to the data. By ethical and legal requirement, specifics of the dataset remain unknown to the researchers.

For purposes of this experiment the data has been split into 3 chunks:

- The `training set`, used to train SimFL
- The `validation set`, used to understand model performance
- The `test set`, used to generate predictions and shapley values on most recent cases to be consumed by NGOs in the federation

## Evaluation Results

### SimFL SCL Only  Results

| Model    | Avg. Precision | Avg. Recall |
| :------- | :------------- | :---------- |
| Baseline | 0.07           |             |
| KPMG     | 0.01           |             |
| SAIL     | 0.12           | 0.06        |

#### KPMG Precision/ Recall Curve 
<p align="left">
    <img src="images\SCL_KPMG_AUC.PNG" height=150> 
</p>

#### SAIL Precision/ Recall Curve
<p align="left">
    <img src="images\SCL_only_AUC.PNG" height=150>
</p>




### SimFL GFR only Evaluation Results

| Model    | Avg. Precision | Avg. Recall |
| :------- | :------------- | :---------- |
| Baseline | 0.015          |             |
| KPMG     | 0.03           |             |
| SAIL     | 0.38           | 0.013       |

#### KPMG Precision/ Recall Curve 
<p align="left">
    <img src="images\GFR_KPMG_AUC.PNG" height=150> 
</p>

#### SAIL Precision/ Recall Curve
<p align="left">
    <img src="images\GFR_only_AUC.PNG" height=150>
</p>

### SIMFL Federated Evaluation Results

| Model           | Avg. Precision | Avg. Recall |
| :-------------- | :------------- | :---------- |
| Baseline        | 0.011          |             |
| Optimised Model | 0.0796         | 0.026       |

#### Optuna Optimised Model
<p align="left">
    <img src="images\federated_optimised_AUC.PNG" height=150>
</p>

### Discussion

While it was possible to train remotely on datasets SCL and GFR using the SAIL platform, training results were far from ideal. In all cases the baseline model was exceeded but predictive performance is poor. With this being said, it is unclear at this stage whether the data in SCL and GFR has the potential to effectively predict customer churn. This should be a topic of investigation for iteration 2.

The results produced by KPMG under ideal conditions were roughly matched by the experiments run on the individual datasets. However, the trained model is less performant on both datasets than the SCL predictor is alone. That being said, it is likely that the GFR NGO will benefit from the predictive power of the SCL dataset.

#### Algorithm Resource Efficiency Issues

While consistent with centralized learning, SimFL was found to be quite inefficient when processing larger datasets. Intensive memory usage makes this build unstable. A lack of parallelization makes it slow to run to completion. This severely inhibits our ability ot run hyperparameter optimization over a large number of iterations. This is an issue which will be resolved by SAIL in future iterations.


### Feature Engineering Output

There are a number of points where we believe we could improve the model performance by enhancing the feature engineering sections.

#### Improved Data Imputation
The first of these is that there are a large number of NaN values in the dataset. NaN values cannot be hashed properly by SimFL and so we change all NaN values to 0. However, it would be to the advantage of the study of these data points were to be imputed with something meaningful for that column, for example the mean value.

#### Dataset Incongruence
The predictive performance of the federated model can partially be explained by structural dissimilarities between datasets SCL and GFR. Further investigation should go into this by the data owner federation. While we were able to pick up on this potential through disparities in the comparsion of SHAP bee swarm plots (See below). While differences in SHAP output can be explained through covariance between features in specific examples, it can also mean that the structure learned by the model is incongruent. our abilities to accurately diagnose and fix is limited/ time expensive due to privacy constraints.

<p align=center>
    <img src="images\GFR_SHAP_Beeswarm.png" height=200>
    <img src="images\SCL_SHAP_Beeswarm.png" height=200>

#### Potential Date Formatting Logic Error
There is a potential logic error in the way that date is where churn is allocated to dates. This compares year then month. Howeverer, it is unclear whether this compensates for months between November and Feburary where there wil be no wrap around for these months.

```
# Churned within three months
agg_df["is_churned_within3m"] = np.where((agg_df['CancelDate_y_min'].dt.year <= agg_df["PaymentDate_"].dt.year) &
                                   (agg_df['CancelDate_y_min'].dt.month <= agg_df["PaymentDate_"].dt.month+3), True, False)
```

#### Covid Data Drift
A time series model may be frustrated by a change in consumer behaviour over the last year. Covid has likely caused new competition between NGOs which may skew instances gathered more recently. This is likely compounded by the economic impact of the virus. This likely a source of data drift. We can avoid this by trimming a large amount of the old data. 

#### Feature Reduction
Currently we run the model over 80 features. However, according to our SHAP plots, a large number of these are not useful. We would recommend making a cut-off to just the features included in the diagram below. Unnecessary features create unnecessary noise for the model to deal with. We recommend you choose only a minority of these features. Below they are listed in order of importance.

<p align=center>
    <img src="images\too_many_features.png" style="transform:rotate(270deg);" height=400>
<p>


#### Conclusions

Our SimFL learning model was able to successfully train in the distributed learning environment and exceed the performance of the baseline. The extent to which this was exceeded is low but consistent with centralised learning. The federated learning model was more performant than GFR but less performant when predicting upon SCL. However, this is likely due to poor predictive power of GFR. It is unclear to us at this time whether the datasets contain enough information to effectively predict customer churn. 


## Deliverable Checklist
- ```Fed_NGOs``` 
  - ```hyperparameter_opt_clean.ipynb``` containing results for the single training example

  - ```study_federated_SCL_GFR.pkl``` a pickled ```Optuna``` study object used to reinitiate the hyperparameter optimisation after termination.
  - ```predictions_federated_optimised_shap_GFR_test.csv```, containing predictions and shap values corresponding to the predictions of the test dataset of GFR, to be consumed by GFR.
  - ```predictions_federated_optimised_shap_SCL_test.csv```, containing predictions and shap values corresponding to the predictions of the test dataset of GFR, to be consumed by SCL.  
- ```SCL_only```
  - ```orchestrator_Federated_clean.ipynb```, contains results from training SimFL on only SCL.
  - ```predictions_shap_SCL_test.csv```, contains predictions and shap values corresponding to SCL test.
- ```GFR_only```
  - ```orchestrator_Federated_clean.ipynb```, contains results from training SimFL on only SCL.
  - ```predictions_shap_GFR_test.csv```, contains predictions and shap values corresponding to SCL test.
