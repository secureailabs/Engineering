from typing import Dict, List, Tuple, Type
import pandas as pd
from zero import SecretObject
import numpy as np
from scipy import stats
import math

def chi_square(sample_0: Type[SecretObject], sample_1: List) -> Dict:
    sample_0 = sample_0.tolist()
    precompute = {}
    for tuple_value in zip(sample_0, sample_1):
        if not tuple_value in precompute:
            precompute[tuple_value] = 0
        precompute[tuple_value] = precompute[tuple_value] + 1
    return precompute

def chi_square_agg(list_precompute: List) -> Dict:
    list_unique_0 = []
    list_unique_1 = []
    for precompute in list_precompute:
        for tuple_value in precompute:
            value_0 = tuple_value[0]
            value_1 = tuple_value[1]
            if not value_0 in list_unique_0:
                list_unique_0.append(value_0)
            if not value_1 in list_unique_1:
                list_unique_1.append(value_1)

    array_true = np.zeros((len(list_unique_0), len(list_unique_1)))
    array_pred = np.zeros((len(list_unique_0), len(list_unique_1)))
    count_total = 0
    for precompute in list_precompute:
        for tuple_value in precompute:
            value_0 = tuple_value[0]
            value_1 = tuple_value[1]
            index_0 = list_unique_0.index(value_0)
            index_1 = list_unique_1.index(value_1)
            array_true[index_0, index_1] += precompute[tuple_value]
            count_total += precompute[tuple_value]

    for i_0 in range(array_true.shape[0]):
        for i_1 in range(array_true.shape[1]):
            array_pred[i_0, i_1] = array_true[i_0, :].sum() * array_true[:, i_1].sum() / count_total

    array_true = array_true.ravel()
    array_pred = array_pred.ravel()
    chisquare_statistic = (np.power(array_true - array_pred, 2) / array_pred).sum()
    degrees_of_freedom = (len(list_unique_0) - 1) * (len(list_unique_1) - 1)

    p_value = stats.distributions.chi2.sf(chisquare_statistic, degrees_of_freedom)
    return (chisquare_statistic, p_value)

def kolmogorov_smirnovdef(sample_0: Type[SecretObject], sample_ranked_0: Type[SecretObject], distribution: str, count_total: int) -> List[float]:
    type_distribution = distribution["type_distribution"]

    array_sample_0 = sample_0.to_numpy()
    array_sample_ranked_0 = sample_ranked_0.to_numpy()

    if type_distribution == "normal":
        sample_mean = np.mean(array_sample_0)
        sample_sdev = np.std(array_sample_0, ddof=1)
        array_value_cdf = stats.norm.cdf(array_sample_0, loc=sample_mean, scale=sample_sdev)
    elif type_distribution == "normalunit":
        array_value_cdf = stats.norm.cdf(array_sample_0, loc=0, scale=1)
    else:
        raise Exception()
    return np.max(np.abs((array_sample_ranked_0 / count_total) - array_value_cdf)).item()

def kolmogorov_smirnovdef_agg(list_precompute: List[float])-> float:
    list_max = []
    for precompute in list_precompute:
        list_max.append(precompute)

    return max(list_max)

def kurtosis(sample_0_dataframe: Type[SecretObject]) -> List[float]:
    """Generates the geometric moments for use in a Kurtosis
    Parameters
    ----------
    sample_0_dataframe : pd.DataFrame
        The dataframe for sample_0
    Returns
    -------
    a list of 3 floats precomputes value
    """

    sample_0 = sample_0_dataframe.to_numpy()
    # First
    sum_x_0 = np.sum(sample_0)
    # second
    sum_xx_0 = np.sum(sample_0 * sample_0)
    # Third
    sum_xxx_0 = np.sum(sample_0 * sample_0 * sample_0)
    # Fourth
    sum_xxxx_0 = np.sum(sample_0 * sample_0 * sample_0 * sample_0)
    # Sample size
    count_0 = len(sample_0)

    list_precompute = [sum_x_0.item(), sum_xx_0.item(), sum_xxx_0.item(), sum_xxxx_0.item(), count_0]

    return list_precompute

def kurtosis_agg(list_list_precompute: List[List[float]]) -> float:

    """
    A Function to get the fedrated Kurtosis value.
    same as scipy.skewsnes ()
    :param list_list_precompute: compute from different DF
    :type list_list_precompute: List[List[float]]
    :return: Kurtosis Value
    :rtype: Float
    """

    sum_x_0 = 0
    sum_xx_0 = 0
    sum_xxx_0 = 0
    sum_xxxx_0 = 0
    size_sample_0 = 0
    # Combining precompute
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        sum_xxx_0 += list_precompute[2]
        sum_xxxx_0 += list_precompute[3]
        size_sample_0 += list_precompute[4]  # same as Count_0

    # Calculating sampel mean
    sample_mean_0 = sum_x_0 / size_sample_0
    # Calculating sample varriance
    sample_varriance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
    # Calculating Sample
    sample_standard_deviation = math.sqrt(sample_varriance_0)

    # mu Geometric
    mu2 = sum_xx_0 / size_sample_0
    mu3 = sum_xxx_0 / size_sample_0
    mu4 = sum_xxxx_0 / size_sample_0
    mean = sample_mean_0
    sd = sample_standard_deviation

    # Final Statistical formula for calculating Kurtosis
    # wiki link below for the formula
    # https://en.wikipedia.org/wiki/Kurtosis

    kurtosis_value = ((mu4) - 3 * (mean**4) - 4 * ((mu3) * (mean)) + 6 * ((mu2) * (mean**2))) / (sd**4)

    return kurtosis_value - 3

def levene(
        sample_0_series: Type[SecretObject], sample_1_series: List, mean_0: float, mean_1: float
    ) -> Tuple[List[float], List[bool]]:  # there seems to be a problem here with this annotation
    """
    ----------
    sample_0_series : pd.Series
        The series for sample_0
    sample_1_series : pd.Series
        The series for sample_1
    Returns
    -------
    a list of 6 floats, two moments for sample_0 followed by the size of sample_0 and two moments for sample_1 followed by the size of sample 1
    """
    sample_1 = np.array(sample_1_series)

    sample_0 = sample_0_series.to_numpy()
    #sample_1 = sample_1_series.to_numpy()

    sum_x_0 = np.sum(sample_0)
    sum_xx_0 = np.sum(sample_0 * sample_0)
    count_0 = len(sample_0)

    sum_x_1 = np.sum(sample_1)
    sum_xx_1 = np.sum(sample_1 * sample_1)
    count_1 = len(sample_1)

    z1j = abs(sample_0 - mean_0)
    z2j = abs(sample_1 - mean_1)

    list_precompute = [sum_x_0.item(), sum_xx_0.item(), count_0, sum_x_1.item(), sum_xx_1.item(), count_1, z1j.tolist(), z2j.tolist()]

    return list_precompute

def levene_agg(
        list_list_precompute: List[List[float]],
        equal_varriances: bool = False,
    ) -> Tuple[float, float]:
    sum_x_0 = 0
    sum_xx_0 = 0
    size_sample_0 = 0
    sum_x_1 = 0
    sum_xx_1 = 0
    size_sample_1 = 0
    final_z1j = []
    final_z2j = []
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        size_sample_0 += list_precompute[2]
        sum_x_1 += list_precompute[3]
        sum_xx_1 += list_precompute[4]
        size_sample_1 += list_precompute[5]
        final_z1j.extend(list_precompute[6])
        final_z2j.extend(list_precompute[7])

    z1_ = np.mean(final_z1j)
    z2_ = np.mean(final_z2j)

    z__ = (z1_ + z2_) / 2

    denom_1 = final_z1j - z1_
    denom_1 = np.sum(denom_1 * denom_1)

    denom_2 = final_z2j - z2_
    denom_2 = np.sum(denom_2 * denom_2)

    final_denom = denom_1 + denom_2
    length1 = size_sample_0
    length2 = size_sample_1
    dof = length1 + length2 - 2
    final_nem = dof * (length1 * (z1_ - z__) * (z1_ - z__) + length2 * (z2_ - z__) * (z2_ - z__))

    f_statictic = final_nem / final_denom

    return (f_statictic, dof)

def mann_whitney(series_0: Type[SecretObject], series_concatenated_ranked: Type[SecretObject]) -> float:
    return series_concatenated_ranked[: series_0.size].sum()

def mann_whitney_agg(list_precompute: List[float]) -> float:
    return np.array(list_precompute).sum()

def mean(
        sample_0_dataframe: Type[SecretObject],
    ) -> Tuple[List[float], List[bool]]:  # there seems to be a problem here with this annotation
    sample_0 = sample_0_dataframe.to_numpy()

    sum_x_0 = np.sum(sample_0)
    sample_0_dof = len(sample_0)

    list_precompute = [sum_x_0.item(), sample_0_dof]
    # list_safe = [False, False, False, False, False, False ]
    return list_precompute

def mean_agg(list_list_precompute: List[List[float]]) -> float:
    sum_x_0 = 0
    dof_0 = 0

    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        dof_0 += list_precompute[1]

    sample_mean_0 = sum_x_0 / dof_0

    # if degrees_of_freedom < 20:
    #     raise Exception()
    return sample_mean_0

def min_max(series_sample: Type[SecretObject]) -> Tuple[float, float]:
    """This function is designed to counteract disclosure of the min and max while giving them estimates that
    are independant for sample size bigger than 2. The function guarantees that min <= sample_min and sample_max <= max
    For uniform distributions this follows the UMVU-estimator altough with bigger varriance
    For normal distribution this creates a min and a max that are far outside the sample
    min and max to protect outliers.
    TODO this function can be improved by doing the actual estimation in the agregate section
    :param series_sample: the sample from witch to estimate the min and max
    :type series_sample: pd.Series
    :raises ValueError: raises a ValueError if the series contains `na` values
    :return: The min and max estimate from the series
    :rtype: Tuple[float, float]
    """
    if 0 < series_sample.isna().sum():
        raise ValueError("Sample contains `na` values")
    array_sample = np.array(series_sample.sort_values(ascending=True, inplace=False))
    subsample_size = int(np.ceil(np.sqrt(series_sample.size)))
    subsample_min = array_sample[:subsample_size]
    subsample_max = array_sample[-subsample_size:]
    subsample_min_width = np.max(subsample_min) - np.min(subsample_min)
    estimate_min = np.min(subsample_min) - (subsample_min_width**2 / series_sample.size)
    subsample_max_width = np.max(subsample_max) - np.min(subsample_max)
    estimate_max = np.max(subsample_max) + (subsample_max_width**2 / series_sample.size)
    return (estimate_min.item(), estimate_max.item())

def min_max_agg(list_tuple_min_max: List[Tuple[float, float]]) -> Tuple[float, float]:
    """Agregates the results of multiple precompute functions into a global min and max
    :param list_tuple_min_max: A list of tuples from various precompute functions
    :type list_tuple_min_max: List[Tuple[float, float]]
    :return: return the federated estimated sample min max
    :rtype: Tuple[float, float]
    """
    list_min = []
    list_max = []
    for tuple_min_max in list_tuple_min_max:
        list_min.append(tuple_min_max[0])
        list_max.append(tuple_min_max[1])
    return (min(list_min), max(list_max))

def paired_t(sample_0_series: Type[SecretObject], sample_1_series: List) -> List[float]:
    """Generates the geometric moments for use in a T-Test
    :param sample_0_series:  The series for sample_0
    :type sample_0_series: pd.Series
    :param sample_1_series: The series for sample_1
    :type sample_1_series: pd.Series
    :return: a list of 3 floats, two moments for sample_d followed by the size of sample_d
    :rtype: List[float]
    """
    sample_1 = np.array(sample_1_series)

    sample_0 = sample_0_series.to_numpy()
    #sample_1 = sample_1_series.to_numpy()
    sample_d = sample_0 - sample_1
    sum_d_0 = np.sum(sample_d)
    sum_dd_0 = np.sum(sample_d * sample_d)
    count_d = len(sample_d)

    list_precompute = [sum_d_0.item(), sum_dd_0.item(), count_d]

    return list_precompute

def paired_t_agg(list_list_precompute: List[List[float]]) -> Tuple[float, float]:
    """collects the parts of a t-test and agregates them into statisitcs
    :param list_list_precompute: a list of 3 floats; two moments for sample_d followed by the size of paired sample
    :type list_list_precompute: List[List[float]]
    :return: returns a t-statistic and its effect size
    :rtype: Tuple[float, float]
    """
    sum_d_0 = 0
    sum_dd_0 = 0
    size_sample_d = 0

    for list_precompute in list_list_precompute:
        sum_d_0 += list_precompute[0]
        sum_dd_0 += list_precompute[1]
        size_sample_d += list_precompute[2]

    sample_mean_d = sum_d_0 / size_sample_d
    sample_varriance_d = ((sum_dd_0 / size_sample_d) - (sample_mean_d * sample_mean_d)) * (
        size_sample_d / (size_sample_d - 1)  # unbiased estimator (numpy version is biased by default)
    )

    t_statistic = sample_mean_d / (np.sqrt(sample_varriance_d) / np.sqrt(size_sample_d))
    degrees_of_freedom = size_sample_d - 1

    # TODO we need to enable this when error handling is implemented
    # if degrees_of_freedom < 20:
    #     raise Exception()
    return (t_statistic, degrees_of_freedom)

def pearson(sample_0_dataframe: Type[SecretObject], sample_1_dataframe: Type[SecretObject]) -> List[float]:
    """
    Parameters
    ----------
    sample_0_dataframe : pd.DataFrame
        The dataframe for sample_0
    sample_1_dataframe : pd.DataFrame
        The dataframe for sample_1
    Returns
    -------
    a list of 6 floats
    """
    sample_0 = sample_0_dataframe.to_numpy()
    sample_1 = sample_1_dataframe.to_numpy()

    sum_x_0 = np.sum(sample_0)
    sum_xx_0 = np.sum(sample_0 * sample_0)
    sample_0_dof = len(sample_0)

    sum_x_1 = np.sum(sample_1)
    sum_xx_1 = np.sum(sample_1 * sample_1)
    sample_1_dof = len(sample_1)

    sum_x1_into_x2 = np.sum(np.multiply(sample_0, sample_1))

    list_precompute = [sum_x_0.item(), sum_xx_0.item(), sample_0_dof, sum_x_1.item(), sum_xx_1.item(), sample_1_dof, sum_x1_into_x2.item()]

    # list_safe = [False, False, False, False, False, False ]
    return list_precompute

def pearson_agg(list_list_precompute: List[List[float]]) -> Tuple[float, int]:
    """
    This function run to calculate the final precompute
    and calculate the federated pearson value.
    :param list_list_precompute:
    :type list_list_precompute: List[List[float]]
    :return: Pearson value r
    :rtype: float
    """
    sum_x_0 = 0
    sum_x_1 = 0
    sum_xx_0 = 0
    sum_xx_1 = 0
    sum_x1_into_x2 = 0
    size_sample_0 = 0
    size_sample_1 = 0
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        size_sample_0 += list_precompute[2]
        sum_x_1 += list_precompute[3]
        sum_xx_1 += list_precompute[4]
        size_sample_1 += list_precompute[5]
        sum_x1_into_x2 += list_precompute[6]

    # Calculating for the first column
    # Calculating sampel mean
    sample_mean_0 = sum_x_0 / size_sample_0
    # Calculating sample varriance
    sample_varriance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
    # Calculating Sample
    sample_standard_deviation_0 = math.sqrt(sample_varriance_0)
    # Calculating for the second column
    # Calculating sampel mean
    sample_mean_1 = sum_x_1 / size_sample_1
    # Calculating sample varriance
    sample_varriance_1 = (sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)
    # Calculating Sample
    sample_standard_deviation_1 = math.sqrt(sample_varriance_1)

    E_xy = sum_x1_into_x2 / size_sample_0

    rho = (E_xy - (sample_mean_0 * sample_mean_1)) / (sample_standard_deviation_0 * sample_standard_deviation_1)
    degrees_of_freedom = size_sample_0 - 2
    return (rho, degrees_of_freedom)

def skewness(sample_0_dataframe: Type[SecretObject]) -> List[float]:
    """Generates the geometric moments for use in a Skewness
    Parameters
    ----------
    sample_0_dataframe : pd.DataFrame
        The dataframe for sample_0
    Returns
    -------
    a list of 3 floats precompute value
    """

    sample_0 = sample_0_dataframe.to_numpy()
    # First
    sum_x_0 = np.sum(sample_0)
    # second
    sum_xx_0 = np.sum(sample_0 * sample_0)
    # Third
    sum_xxx_0 = np.sum(sample_0 * sample_0 * sample_0)
    # Sample size
    count_0 = len(sample_0)

    list_precompute = [sum_x_0.item(), sum_xx_0.item(), sum_xxx_0.item(), count_0]

    return list_precompute

def skewness_agg(list_list_precompute: List[List[float]]) -> float:

    """
    A Function to get the fedrated skewness value.
    same as scipy.skewsnes ()
    :param list_list_precompute: compute from different DF
    :type list_list_precompute: List[List[float]]
    :return: Skewness Value
    :rtype: Float
    """

    sum_x_0 = 0
    sum_xxx_0 = 0
    sum_xx_0 = 0
    size_sample_0 = 0
    # Combining precompute
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        sum_xxx_0 += list_precompute[2]
        size_sample_0 += list_precompute[3]  # same as Count_0

    # Calculating sampel mean
    sample_mean_0 = sum_x_0 / size_sample_0
    # Calculating sample varriance
    sample_varriance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
    # Calculating Sample
    sample_standard_deviation = math.sqrt(sample_varriance_0)
    # mu3 Geometric
    mu3 = sum_xxx_0 / size_sample_0
    mean = sample_mean_0
    sd = sample_standard_deviation
    # Final Statistical formula for calculating skewness
    # wiki link below for the formula
    # https://en.wikipedia.org/wiki/Skewness
    skewness_value = (mu3 - (3 * mean * sd * sd) - mean**3) / (sd**3)

    return skewness_value

def unpaired_t(sample_0_series: Type[SecretObject], sample_1_series: List) -> List[float]:
    """Generates the geometric moments for use in a T-Test
    Parameters
    ----------
    sample_0_series : pd.Series
        The series for sample_0
    sample_1_series : pd.Series
        The series for sample_1
    Returns
    -------
    a list of 6 floats, two moments for sample_0 followed by the size of sample_0 and two moments for sample_1 followed by the size of sample 1
    """
    sample_1 = np.array(sample_1_series)
    
    sample_0 = sample_0_series.to_numpy()
    #sample_1 = sample_1_series.to_numpy()

    sum_x_0 = np.sum(sample_0)
    sum_xx_0 = np.sum(sample_0 * sample_0)
    count_0 = len(sample_0)

    sum_x_1 = np.sum(sample_1)
    sum_xx_1 = np.sum(sample_1 * sample_1)
    count_1 = len(sample_1)

    list_precompute = [sum_x_0.item(), sum_xx_0.item(), count_0, sum_x_1.item(), sum_xx_1.item(), count_1]

    return list_precompute

def unpaired_t_agg(
        list_list_precompute: List[List[float]],
        equal_varriances: bool = False,
    ) -> Tuple[float, float]:
    sum_x_0 = 0
    sum_xx_0 = 0
    size_sample_0 = 0
    sum_x_1 = 0
    sum_xx_1 = 0
    size_sample_1 = 0
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        size_sample_0 += list_precompute[2]
        sum_x_1 += list_precompute[3]
        sum_xx_1 += list_precompute[4]
        size_sample_1 += list_precompute[5]

    sample_mean_0 = sum_x_0 / size_sample_0
    sample_varriance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
        size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
    )

    sample_mean_1 = sum_x_1 / size_sample_1
    sample_varriance_1 = ((sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)) * (
        size_sample_1 / (size_sample_1 - 1)  # unbiased estimator (np version is biased by default)
    )

    if equal_varriances:
        sample_varriance_pooled = (
            ((size_sample_0 - 1) * sample_varriance_0) + ((size_sample_1 - 1) * sample_varriance_1)
        ) / (size_sample_0 + size_sample_1 - 2)
        t_statistic = (sample_mean_0 - sample_mean_1) / (
            np.sqrt(sample_varriance_pooled) * np.sqrt((1 / size_sample_0 + 1 / size_sample_1))
        )
        degrees_of_freedom = size_sample_0 + size_sample_1 - 2

    else:
        # sample_varriance_0 /= size_sample_0 / (size_sample_0 - 1)
        # sample_varriance_1 /= size_sample_1 / (size_sample_1 - 1)
        t_statistic = (sample_mean_0 - sample_mean_1) / (
            np.sqrt((sample_varriance_0 / size_sample_0) + (sample_varriance_1 / size_sample_1))
        )
        # Welch–Satterthwaite equation:
        dof_nominator = math.pow(((sample_varriance_0 / size_sample_0) + (sample_varriance_1 / size_sample_1)), 2)
        dof_denominator = (
            math.pow(sample_varriance_0, 2) / (size_sample_0 * size_sample_0 * (size_sample_0 - 1))
        ) + (math.pow(sample_varriance_1, 2) / (size_sample_1 * size_sample_1 * (size_sample_1 - 1)))
        degrees_of_freedom = dof_nominator / dof_denominator

    # if degrees_of_freedom < 20:
    #     raise Exception()
    return (t_statistic, degrees_of_freedom)

def variance(
        sample_0: Type[SecretObject],
    ) -> Tuple[List[float], List[bool]]:  # there seems to be a problem here with this annotation
    sample_0 = sample_0.to_numpy()

    sum_x_0 = np.sum(sample_0)
    sum_xx_0 = np.sum(sample_0 * sample_0)
    sample_0_dof = len(sample_0)

    list_precompute = [sum_x_0.item(), sum_xx_0.item(), sample_0_dof]
    return list_precompute

def variance_agg(list_list_precompute: List[List[float]]) ->float:
    sum_x_0 = 0
    sum_xx_0 = 0
    size_sample_0 = 0

    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        size_sample_0 += list_precompute[2]

    sample_mean_0 = sum_x_0 / size_sample_0

    sample_varriance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
        size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
    )

    return sample_varriance_0

def wilcoxon_signed_rank(sample_difference: Type[SecretObject], sample_absolute_difference_ranked: Type[SecretObject]) -> List[float]:
    rank_minus = np.sum((sample_difference.to_numpy() < 0) * sample_absolute_difference_ranked.to_numpy())
    rank_plus = np.sum((sample_difference.to_numpy() > 0) * sample_absolute_difference_ranked.to_numpy())
    return [rank_minus.item(), rank_plus.item()]

def wilcoxon_signed_rank_agg(list_precompute: List) -> Tuple[float]:
    rank_minus = 0
    rank_plus = 0
    for precompute in list_precompute:
        rank_minus += precompute[0]
        rank_plus += precompute[1]
    return (rank_minus, rank_plus)