# Imports
import sys
import numpy as np

def max_emd_from_shape(action_space_shape):
    """
    Computes the maximum possible Earth Mover's Distance (EMD) for a given array shape.

    Parameters:
        array_shape (tuple): Shape of the numpy array.

    Returns:
        int: Maximum EMD value possible within the space.
    """
    if not isinstance(action_space_shape, (tuple, list)) or len(action_space_shape) == 0:
        raise ValueError("Input must be a non-empty tuple or list representing the array shape.")
    
    # Compute max index difference for each dimension
    max_differences = np.array(action_space_shape) - 1
    
    # Sum of all absolute index differences gives the max EMD
    max_emd = np.sum(max_differences)

    return max_emd


def calculate_distance(distance_type="none", np_a=None, np_b=None, action_space_shape=None):
    """
    Calculate distance between two numpy arrays based on the selected method.

    Parameters:
        distance_type (str): The type of distance calculation. Options are 'none', 'emd', or 'kinematic'.
        np_a (np.ndarray): First input numpy array containing integers.
        np_b (np.ndarray): Second input numpy array containing integers.

    Returns:
        float: Computed distance value based on the method selected.
    """

    # CHECKS
    # Ensure inputs are numpy arrays
    if not isinstance(np_a, np.ndarray) or not isinstance(np_b, np.ndarray):
        raise ValueError("Both inputs must be numpy arrays.")
    
    # Ensure both arrays have the same shape
    if np_a.shape != np_b.shape:
        raise ValueError("Input arrays must have the same shape.")

    # Ensure all elements in the arrays are integers
    if not np.issubdtype(np_a.dtype, np.integer) or not np.issubdtype(np_b.dtype, np.integer):
        raise ValueError("Both numpy arrays must contain integer values.")

    # Ensure array_space is provided for EMD calculation
    if distance_type == "emd" and action_space_shape is None:
        raise ValueError("Shape of the action space must be provided for EMD calculation.")

    # DISTANCE CALCULATION
    # Case 1: No distance calculation
    if distance_type == "none":
        return 0

    # Case 2: Earth Mover's Distance (EMD) approximation
    elif distance_type == "emd":
        emd_distance = np.sum(np.abs(np_a - np_b))

        # Normalize the EMD value
        max_emd = max_emd_from_shape(action_space_shape)
        normmalized_emd = emd_distance / max_emd

        # # sanity check that normalized EMD is between 0 and 1
        # if normmalized_emd < 0 or normmalized_emd > 1:
        #     raise ValueError("Normalized EMD value must be between 0 and 1.")

        # print("emd_distance:", emd_distance)
        # print("max_emd:", max_emd)
        # print("normmalized_emd:", normmalized_emd)

        return normmalized_emd

    # Case 3: Kinematic distance (to be implemented)
    elif distance_type == "kinematic":

        # pull in kinematic distance array, each entry of this array being a dictionary with 12 entries (one for each joint), each dictionary element being a list of 3 floats representing the joint's XYZ position 
        # calculate the maximum distance between the two arrays within this kinematic distance array
            # if we need to make this more efficient, we can simply use the 3^4 = 81 possible combinations of the 4 joints and calculate the distance between each of these combinations
        # calculate the distance between the two specific elements of this array with the index np_a and np_b
        # scale this distance to be between 0 and 1 
        # return the scaled distance between the two specific elements of this array with the index np_a and np_b

        return 'kinematic output placeholder'  # Placeholder for future implementation

    else:
        raise ValueError("Invalid distance_type. Choose from 'none', 'emd', or 'kinematic'.")



# Example usage
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "test":

    test_action_space_shape = (3, 3, 3, 3, 3)

    np_a = np.array([2, 2, 2, 2, 2])
    np_b = np.array([0, 0, 0, 0, 0])

    print("Input arrays:")
    print("np_a shape", np_a.shape)
    print("np_b shape", np_b.shape)

    print("None distance:", calculate_distance(distance_type="none", np_a=np_a, np_b=np_b))  
    print("EMD distance:", calculate_distance(distance_type="emd", np_a=np_a, np_b=np_b, action_space_shape=test_action_space_shape))
    print("Kinematic distance:", calculate_distance(distance_type="kinematic", np_a=np_a, np_b=np_b))  # Placeholder



