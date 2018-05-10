import numpy as np
from scipy.stats import chisquare
from scipy.stats.distributions  import chi2
def gtest(f_obs, f_exp=None, ddof=0):
    """
    http://en.wikipedia.org/wiki/G-test
    The G test can test for goodness of fit to a distribution
    Parameters
    ----------
    f_obs : array
        observed frequencies in each category
    f_exp : array, optional
        expected frequencies in each category.  By default the categories are
        assumed to be equally likely.
    ddof : int, optional
        adjustment to the degrees of freedom for the p-value
    Returns
    -------
    chisquare statistic : float
        The chisquare test statistic
    p : float
        The p-value of the test.
    Notes
    -----
    The p-value indicates the probability that the observed distribution is
    drawn from a distribution given frequencies in expected.
    So a low p-value inidcates the distributions are different.
    Examples
    --------
    >>> gtest([9.0, 8.1, 2, 1, 0.1, 20.0], [10, 5.01, 6, 4, 2, 1])
    (117.94955444335938, 8.5298516190930345e-24)
    >>> gtest([1.01, 1.01, 4.01], [1.00, 1.00, 4.00])
    (0.060224734246730804, 0.97033649350189344)
    >>> gtest([2, 1, 6], [4, 3, 2])
    (8.2135343551635742, 0.016460903780063787)
    References
    ----------
    http://en.wikipedia.org/wiki/G-test
    """
    f_obs = [i if i!=0 else 1e-10 for i in f_obs]
    f_obs = np.asarray(f_obs, 'f')
    k = f_obs.shape[0]
    f_exp = np.array([np.sum(f_obs, axis=0) / float(k)] * k, 'f') \
                if f_exp is None \
                else np.asarray(f_exp, 'f')
    g = 2 * np.add.reduce(f_obs * np.log(f_obs / f_exp))
    return g, chi2.sf(g, k - 1 - ddof)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
