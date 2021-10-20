import numpy as np


class ConnectivityCalculator:

    connectivity = {}

    @classmethod
    def calculate_connectivity(cls, atoms):
        """
        Calculates the connectivity matrix (showing which atoms are bonded as 1 and those that are not bonded as 0.
        It uses the Van Der Waals radius an Atom (see `Atom` class) to determine if atoms should be bonded or not.

        Args:
            :atoms: `Atoms` instance

        Returns:
            :type: `np.ndarray`
                The connectivity matrix between atoms of shape len(atoms) x len(atoms)

        .. note::

            This is a class method because the connectivity only needs to be calculated once per trajectory. The connectivity remains the same for all
            timesteps in a trajectory.
        """

        system_hash = atoms.hash
        if system_hash not in cls.connectivity.keys():
            connectivity = np.zeros((len(atoms), len(atoms)))

            adjus = 0.52917706 # taken from molden6.9/src/getpoi.f:874
            for i, iatom in enumerate(atoms):
                for j, jatom in enumerate(atoms):
                    if iatom != jatom:
                        max_dist = (iatom.vdwr + jatom.vdwr)/adjus
                        max_dist_sq = max_dist * max_dist
                        if (
                            np.linalg.norm(
                                iatom.coordinates - jatom.coordinates
                            )**2
                            < max_dist_sq  # if distance is less than the max_dist, the atoms are bonded, otherwise there are not
                        ):
                            connectivity[i, j] = 1

            cls.connectivity[system_hash] = connectivity

        return cls.connectivity[system_hash]
