from typing import List

import numpy
import pandas
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.statistics.estimator import Estimator
from sail_safe_functions.aggregator.statistics.kolmogorov_smirnov_test import KolmogorovSmirnovTest
from sail_safe_functions.aggregator.statistics.kurtosis import Kurtosis
from sail_safe_functions.aggregator.statistics.mean import Mean
from sail_safe_functions.aggregator.statistics.min_max import MinMax

# import tests
from sail_safe_functions.aggregator.statistics.paired_t_test import PairedTTest
from sail_safe_functions.test.helper_sail_safe_functions.estimator_one_sample_reference import EstimatorReference

# import helper
from sail_safe_functions.test.helper_sail_safe_functions.generator_one_sample_float import GeneratorOneSampleFloat
from sail_safe_functions.test.helper_sail_safe_functions.generator_two_sample_float import GeneratorTwoSampleFloat
from sail_safe_functions.test.helper_sail_safe_functions.participant_service_local import ParticipantSeriviceLocal
from sail_safe_functions.test.helper_sail_safe_functions.tools_accuracy import (
    create_report_power,
    evaluate_accuracy,
    plot_estimator_comparrison,
    plot_report_estimator,
    plot_report_power,
)
from sail_safe_functions.test.helper_sail_safe_functions.tools_privacy import compute_single_knockout_privacy_measure

implementation_manager = ImplementationManager.get_instance()
implementation_manager.set_participant_service(ParticipantSeriviceLocal())
implementation_manager.initialize()

# %%
alternative = "two-sided"
one_sample_normal_high_res = GeneratorOneSampleFloat(
    name="normal unit",
    type_distribution="normal",
    mean=0.0,
    standard_deviation=1.0,
    list_weight_federation=[1.0],
    resolution=-1,
)
one_sample_normal_low_res = GeneratorOneSampleFloat(
    name="normal unit",
    type_distribution="normal",
    mean=0.0,
    standard_deviation=1.0,
    list_weight_federation=[1.0],
    resolution=0.2,
)
one_sample_uniform_high_res = GeneratorOneSampleFloat(
    name="uniform unit",
    type_distribution="uniform",
    mean=0.0,
    standard_deviation=1.0,
    list_weight_federation=[1.0],
    resolution=-1,
)
one_sample_uniform_low_res = GeneratorOneSampleFloat(
    name="uniform unit",
    type_distribution="uniform",
    mean=0.0,
    standard_deviation=1.0,
    list_weight_federation=[1.0],
    resolution=0.2,
)

two_sample_normal_high_res = GeneratorTwoSampleFloat(
    name="normal unit",
    type_distribution="normal",
    mean=0.0,
    standard_deviation=1.0,
    list_weight_federation=[1.0],
    resolution=-1,
)
two_sample_normal_low_res = GeneratorTwoSampleFloat(
    name="normal unit",
    type_distribution="normal",
    mean=0.0,
    standard_deviation=1.0,
    list_weight_federation=[1.0],
    resolution=0.2,
)
two_sample_uniform_high_res = GeneratorTwoSampleFloat(
    name="uniform unit",
    type_distribution="uniform",
    mean=0.0,
    standard_deviation=1.0,
    list_weight_federation=[1.0],
    resolution=-1,
)
two_sample_uniform_low_res = GeneratorTwoSampleFloat(
    name="uniform unit",
    type_distribution="uniform",
    mean=0.0,
    standard_deviation=1.0,
    list_weight_federation=[1.0],
    resolution=0.2,
)


# %%


estimator_ks = KolmogorovSmirnovTest("normalunit", "cdf")
estimator_min_max = MinMax()
estimator_mean = Mean()
estimator_kurtosis = Kurtosis()


# list_sample_size = [5, 10, 15, 20, 25, 50, 100]
list_sample_size = [5, 20, 50]
count_accuracy = 500
count_privacy = 50
print("Generate: report_min_max", flush=True)
report_min_max = evaluate_accuracy(
    estimator_min_max, one_sample_normal_high_res, list_sample_size, count_accuracy, count_privacy
)
print("Generate: report_mean", flush=True)
report_mean = evaluate_accuracy(
    estimator_mean, one_sample_normal_high_res, list_sample_size, count_accuracy, count_privacy
)
print("Generate: report_kurtosis", flush=True)
report_kurtosis = evaluate_accuracy(
    estimator_kurtosis, one_sample_normal_high_res, list_sample_size, count_accuracy, count_privacy
)
print("Generate: report_ks", flush=True)
report_ks = evaluate_accuracy(estimator_ks, one_sample_normal_high_res, list_sample_size, count_accuracy, count_privacy)


plot_report_estimator("MinMax with normal distribution", report_min_max)
plot_report_estimator("Mean with normal distribution", report_mean)
plot_report_estimator("Kurtosis with normal distribution", report_kurtosis)
plot_report_estimator("KolmogorovSmirnov with normal distribution", report_ks)


plot_estimator_comparrison(
    [
        (report_min_max, "min"),
        (report_min_max, "max"),
        (report_ks, "k_statistic"),
        (report_mean, "mean"),
        (report_kurtosis, "kurtosis"),
    ]
)


import plotly.graph_objects as go

# %%

list_sample_size = [5, 10, 15, 25, 50]
list_effect_size = [0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
is_paired = False
significance = 0.05
run_count = 200


estimator = PairedTTest(alternative="two-sided")
report_power = create_report_power(
    estimator, two_sample_normal_high_res, list_sample_size, list_effect_size, is_paired, significance, run_count
)
plot_report_power(report_power, "Power anaysis for Paired t test on normal high res data")
report_power = create_report_power(
    estimator, two_sample_normal_low_res, list_sample_size, list_effect_size, is_paired, significance, run_count
)
plot_report_power(report_power, "Power anaysis for Paired t test on normal low res data")
report_power = create_report_power(
    estimator, two_sample_uniform_high_res, list_sample_size, list_effect_size, is_paired, significance, run_count
)
plot_report_power(report_power, "Power anaysis for Paired t test on uniform high res data")
report_power = create_report_power(
    estimator, two_sample_uniform_low_res, list_sample_size, list_effect_size, is_paired, significance, run_count
)
plot_report_power(report_power, "Power anaysis for Paired t test on uniform low res data")


estimator = PairedTTest(alternative="two-sided")
report_power = create_report_power(
    estimator, two_sample_normal_high_res, list_sample_size, list_effect_size, is_paired, significance, run_count
)
plot_report_power(report_power, "Power anaysis for Paired t test on normal high res data")
report_power = create_report_power(
    estimator, two_sample_normal_low_res, list_sample_size, list_effect_size, is_paired, significance, run_count
)
plot_report_power(report_power, "Power anaysis for Paired t test on normal low res data")
report_power = create_report_power(
    estimator, two_sample_uniform_high_res, list_sample_size, list_effect_size, is_paired, significance, run_count
)
plot_report_power(report_power, "Power anaysis for Paired t test on uniform high res data")
report_power = create_report_power(
    estimator, two_sample_uniform_low_res, list_sample_size, list_effect_size, is_paired, significance, run_count
)
plot_report_power(report_power, "Power anaysis for Paired t test on uniform low res data")


# %%
s1, s2 = two_sample_uniform_high_res.generate(10000, 5, True)

import plotly.express as px

fig = px.histogram(x=s1.to_numpy())
fig.show()

fig = px.histogram(x=s2.to_numpy())
fig.show()

fig = px.scatter(x=s1.to_numpy(), y=s2.to_numpy())
fig.show()
