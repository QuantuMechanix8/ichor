import numpy as np

from ichor.models.kernels.distance import Distance
from ichor.models.kernels.kernel import Kernel


class RBFCyclic(Kernel):

    # TODO: figure out a good way to say if training data is standardized, normalized, etc. because this kernel is affected by data preprocessing

    """Implemtation of Radial Basis Function (RBF) kernel with cyclic feature correction for phi angle feature
    
    .. note::
        Cyclic correction is applied only for our phi angles (phi is the azimuthal angle measured in the xy plane).

        If we have unstandardized(original) features, we have to apply this correction only when the distance between two phi angles is greater than pi

        .. math::

            \phi_1 - \phi_2 = \left \{
            \begin{aligned}
            &\phi_1 - \phi_2, && \text{if}\ \phi_1 - \phi_2 \leq \pi \\
            & 2\pi - (\phi_1 - \phi_2), && \text{if}\ (\phi_1 - \phi_2) \geq \pi
            \end{aligned} \right.
        
        If we have standardized features (where we have subtracted the feature mean and divided by the feature standard deviation),
        we have to apply a correction only when the distance is greater than pi/sigma where sigma is the standard deviation of
        the particular feature in the training data.

        .. math::

            \hat \phi_1 - \hat \phi_2 = \left \{
            \begin{aligned}
            &\hat \phi_1 - \hat \phi_2, && \text{if}\ \hat \phi_1 - \hat \phi_2 \leq \frac{\pi}{\sigma} \\
            & \frac{2\pi}{\sigma} - (\hat \phi_1 - \hat \phi_2), && \text{if}\ (\hat \phi_1 - \hat \phi_2) \geq \frac{\pi}{\sigma}
            \end{aligned} \right.    
    """

    def __init__(self, lengthscale: np.ndarray):

        """
        Args:
            :param: `lengthscale` np.ndarray of shape ndimensions (1D array):
                array of lengthscales. We are using a separate lengthscale for each feature(dimension).
            :param: optional, `train_x_std` np.ndarray of shape ndimensions (1D array):
                if training/test data is standardized, then `train_x_std` has to be provided. This array contains the standard
                deviations for each feature, calculated from the training set points.
        """

        self._lengthscale = lengthscale

    @property
    def params(self):
        return self._lengthscale

    def k(self, x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
        """Calcualtes cyclic RBF covariance matrix from two sets of points

        Args:
            :param: `x1` np.ndarray of shape n x ndimensions:
                First matrix of n points
            :param: `x2` np.ndarray of shape m x ndimensions:
                Second marix of m points, can be identical to the first matrix `x1`

        Returns:
            :type: `np.ndarray`
                The cyclic RBF covariance matrix matrix of shape (n, m)
        """

        # work with distance matrices for each dimension(feature) and check which phi matrices if corrections are needed
        # after distance matrices for each dimension are computed(and corrected where needed), divide by lengthscale and square
        dist_corrected = np.zeros((x1.shape[0], x2.shape[0]))

        for dim_idx, (x1_one_dimension, x2_one_dimension) in enumerate(zip(x1.T, x2.T)):
            res = Distance.euclidean_distance(x1_one_dimension, x2_one_dimension)

            if dim_idx > 2 and (dim_idx + 1) % 3 == 0:  # if phi feature
                res = np.where((res > np.pi), (2.0 * np.pi - res), res)

            res = res / self._lengthscale[dim_idx]
            res = np.power(res, 2)

            # accumulate corrected matrix for each feature(dimension) to get the total (corrected) distance between points
            dist_corrected = dist_corrected + res

        return np.exp(-0.5 * dist_corrected)