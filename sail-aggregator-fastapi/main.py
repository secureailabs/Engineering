##################################################
# This file contains the fastapi implementation of the Smart Broker.
# Currently it only includes the statistics functions
##################################################
# Property of Secure AI Labs
##################################################
# Author: Adam J. Hall
# Copyright: Copyright 02/11/2022, MVP Delivery
# Version: 0.0.0
# Mmaintainer: Secure AI Labs
# Email: adam.hall@secureailabs.com
# Status: Alpha
##################################################

from sail_safe_functions.aggregator.statistics.chisquare import Chisquare
from sail_safe_functions.aggregator.statistics.kolmogorov_smirnov_test import KolmogorovSmirnovTest
from sail_safe_functions.aggregator.statistics.kurtosis import Kurtosis
from sail_safe_functions.aggregator.statistics.levene_test import LeveneTest
from sail_safe_functions.aggregator.statistics.mann_whitney_u_test import MannWhitneyUTest
from sail_safe_functions.aggregator.statistics.mean import Mean
from sail_safe_functions.aggregator.statistics.min_max import MinMax
from sail_safe_functions.aggregator.statistics.paired_t_test import PairedTTest
from sail_safe_functions.aggregator.statistics.pearson import Pearson
from sail_safe_functions.aggregator.statistics.skewness import Skewness
from sail_safe_functions.aggregator.statistics.spearman import Spearman
from sail_safe_functions.aggregator.statistics.student_t_test import StudentTTest
from sail_safe_functions.aggregator.statistics.variance import Variance
from sail_safe_functions.aggregator.statistics.wilcoxon_signed_rank_test import WilcoxonSingedRankTest
from SecureUtility import get_series, get_series_different, validate

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
async def root():
    """
    Redirects user to docs as hompage
    """
    return RedirectResponse("/docs")


@app.get("/mean")
async def mean(series_uuid: str) -> dict:
    """
    Returns the mean of the supplied remote series.

    :param: series_uuid: UUID of remote series
    :type: str
    :return: dict containing value of mean
    :type: dict
    """
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = Mean()
    mean_sail = estimator.run(series)

    # Return
    return {"mean_sail": mean_sail}


@app.get("/chisquare")
async def chisquare(series_uuid_1: str, series_uuid_2: str) -> dict:
    """
    Returns the chisquare of the supplied remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :param: series_uuid_2: UUID of second remote series
    :type: str
    :return: dict containing value of chisquare
    :type: dict
    """
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = Chisquare()
    chisquare_sail = estimator.run(series_1, series_2)

    # Return
    return {"chisquare_sail": chisquare_sail}


@app.get("/kolmogorovSmirnovTest")
async def kolmogorovSmirnovTest(series_uuid: str, type_distribution: str, type_ranking: str) -> dict:
    """
    Returns the Kolmogorov Smirnov Test of the supplied remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :param: series_uuid_2: UUID of second remote series
    :type: str
    :return: dict containing k statistic and p value of Kolmogorov Smirnov Test
    :type: dict
    """
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = KolmogorovSmirnovTest(type_distribution=type_distribution, type_ranking=type_ranking)
    k_statistic_sail, p_value_sail = estimator.run(series)

    # Return
    return {"k_statistic_sail": k_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/kurtosis")
async def kurtosis(series_uuid: str) -> dict:
    """
    Returns the kurtosis of the supplied remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :return: dict containing value of kurtosis
    :type: dict
    """
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = Kurtosis()
    kurtosis_sail = estimator.run(series)

    # Return
    return {"kurtosis_sail": kurtosis_sail}


@app.get("/leveneTest")
async def leveneTest(series_uuid_1: str, series_uuid_2: str) -> dict:
    """
    Returns the Levene Test of two remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :param: series_uuid_2: UUID of second remote series
    :type: str
    :return: dict containing f statistic and p value of Levene test
    :type: dict
    """
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = LeveneTest()
    f_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"f_statistic_sail": f_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/mannWhitneyUTest")
async def mannWhitneyUTest(series_uuid_1: str, series_uuid_2: str, alternative: str, type_ranking: str) -> dict:
    """
    Returns the Mann Whitney U Test of two remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :param: series_uuid_2: UUID of second remote series
    :type: str
    :return: dict containing w statistic and p value of the Mann Whitney U Test
    :type: dict
    """
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = MannWhitneyUTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"w_statistic_sail": w_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/minMax")
async def minMax(series_uuid: str) -> dict:
    """
    Returns the Min and Max value of a remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :return: dict containing the min and max value
    :type: dict
    """
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = MinMax()
    min_sail, max_sail = estimator.run(series)

    # Return
    return {"min_sail": min_sail, "max_sail": max_sail}


@app.get("/pairedTTest")
async def pairedTTest(series_uuid_1: str, series_uuid_2: str, alternative: str) -> dict:
    """
    Returns the Paired T Test of two remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :param: series_uuid_2: UUID of second remote series
    :type: str
    :param: alternative: string specifying options for t test can be {"less", "two-sided", "greater"}
    :type: str
    :return: dict containing t statistic and p value
    :type: dict
    """
    # Arrange
    series_1 = get_series()
    series_2 = get_series_different()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = PairedTTest(alternative=alternative)
    t_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"t_statistic_sail": t_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/pearson")
async def pearson(series_uuid_1: str, series_uuid_2: str, alternative: str) -> dict:
    """
    Returns the Pearson statistic of two remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :param: series_uuid_2: UUID of second remote series
    :type: str
    :param: alternative: string specifying options for method can be {"less", "two-sided", "greater"}
    :type: str
    :return: dict containing pearson statistic and p value
    :type: dict
    """
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = Pearson(alternative=alternative)
    pearson_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"pearson_sail": pearson_sail, "p_value_sail": p_value_sail}


@app.get("/skewness")
async def skewness(series_uuid: str) -> dict:
    """
    Returns the Skewness value of a remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :return: dict containing the skewness value
    :type: dict
    """
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = Skewness()
    skewness_sail = estimator.run(series)

    # Return
    return {"skewness_sail": skewness_sail}


@app.get("/spearman")
async def spearman(series_uuid_1: str, series_uuid_2: str, alternative: str, type_ranking: str) -> dict:
    """
    Returns the Spearman of two remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :param: series_uuid_2: UUID of second remote series
    :type: str
    :param: alternative: string specifying options for method can be {"less", "two-sided", "greater"}
    :type: str
    :param: type_ranking: The mode for which to run the ranking algoritm in must be `unsafe` or `cdf` where `unsafe`
        is unsafe and must be refactored out before this ends up in production
    :type: str
    :return: dict containing spearman statistic and p value
    :type: dict
    """
    # Arrange
    series_1 = get_series()
    series_2 = get_series_different()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    spearman_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"spearman_sail": spearman_sail, "p_value_sail": p_value_sail}


@app.get("/studentTTest")
async def studentTTest(series_uuid_1: str, series_uuid_2: str, alternative: str) -> dict:
    """
    Returns the Student T Test of two remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :param: series_uuid_2: UUID of second remote series
    :type: str
    :param: alternative: string specifying options for method can be {"less", "two-sided", "greater"}
    :type: str
    :return: dict containing t statistic and p value
    :type: dict
    """
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = StudentTTest(alternative=alternative)
    t_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"t_statistic_sail": t_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/variance")
async def variance(series_uuid: str) -> dict:
    """
    Returns the Variance value of a remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :return: dict containing the variance value
    :type: dict
    """
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = Variance()
    variance_sail = estimator.run(series)

    # Return
    return {"variance_sail": variance_sail}


@app.get("/welchTTest")
async def welchTTest(series_uuid_1: str, series_uuid_2: str, alternative: str) -> dict:
    """
    Returns the Welch T Test of two remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :param: series_uuid_2: UUID of second remote series
    :type: str
    :param: alternative: string specifying options for method can be {"less", "two-sided", "greater"}
    :type: str
    :return: dict containing t statistic and p value
    :type: dict
    """
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = StudentTTest(alternative=alternative)
    t_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"t_statistic_sail": t_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/wilcoxonSignedRankTest")
async def wilcoxonSignedRankTest(series_uuid_1: str, series_uuid_2: str, alternative: str, type_ranking: str) -> dict:
    """
    Returns the Wilcoxon Signed Rank Test of two remote series.

    :param: series_uuid_1: UUID of first remote series
    :type: str
    :param: series_uuid_2: UUID of second remote series
    :type: str
    :param: alternative: string specifying options for method can be {"less", "two-sided", "greater"}
    :type: str
    :param: type_ranking: The mode for which to run the ranking algoritm in must be `unsafe` or `cdf` where `unsafe`
        is unsafe and must be refactored out before this ends up in production
    :type: str
    :return: dict containing w statistic and p value
    :type: dict
    """
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"w_statistic_sail": w_statistic_sail, "p_value_sail": p_value_sail}
