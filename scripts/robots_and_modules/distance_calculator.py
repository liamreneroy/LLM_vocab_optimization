# Imports
import sys
import numpy as np

def euclidean_distance(pointA, pointB):
    return np.linalg.norm(np.array(pointA) - np.array(pointB))




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




# Iterate through all timesteps
def dynamic_distance_calculator(listA, listB):
    total_distance = 0

    # Ensure listA and listB have the same length
    if len(listA) != len(listB):
        raise ValueError(f"Error: listA and listB must have the same length. Got {len(listA)} and {len(listB)}.")

    # Initialize cumulative distance
    total_distance = 0

    for timestep in range(len(listA)):
        for key in ["QFR", "QFL", "QRR", "QRL"]:  # Iterate over all four keys
            total_distance += euclidean_distance(listA[timestep][key], listB[timestep][key])

    return total_distance




def max_dynamic_distance_calculator(trajectory_array):
    """
    Computes the maximum possible dynamic distance for a given trajectory array.

    Parameters:
        trajectory_array (np.ndarray): Numpy array containing trajectory data.

    Returns:
        int: Maximum dynamic distance possible within the space.
    """

    print("::: Calculated Max Dynamic Distance ... this could take a while :::")
    
    max_dynamic_distance = 0

    # Compare each element against each element in trajectory_array using the function dynamic_distance_calculator(A, B)
    for idx1 in np.ndindex(trajectory_array.shape):
        for idx2 in np.ndindex(trajectory_array.shape):
            dynamic_distance = dynamic_distance_calculator(trajectory_array[idx1], trajectory_array[idx2])

            if dynamic_distance > max_dynamic_distance:
                max_dynamic_distance = dynamic_distance

                print(f'Comparing: {idx1} and {idx2}: {dynamic_distance} ********')
            else:
                print(f'Comparing: {idx1} and {idx2}: {dynamic_distance}')

    print(f"::: Max Dynamic Distance Done: {max_dynamic_distance}")
    return max_dynamic_distance




def calculate_distance(distance_type="none", trajectory_array=None, np_pose_a=None, np_pose_b=None, action_space_shape=None, max_dynamic_distance=None):
    """
    Calculate distance between two numpy arrays based on the selected method.

    Parameters:
        distance_type (str): The type of distance calculation. Options are 'none', 'emd', or 'dynamic'.
        np_pose_a (np.ndarray): First input numpy array containing integers.
        np_pose_b (np.ndarray): Second input numpy array containing integers.

    Returns:
        float: Computed distance value based on the method selected.
    """

    # CHECKS
    # Ensure inputs are numpy arrays
    if not isinstance(np_pose_a, np.ndarray) or not isinstance(np_pose_b, np.ndarray):
        raise ValueError("Both inputs must be numpy arrays.")
    
    # Ensure both arrays have the same shape
    if np_pose_a.shape != np_pose_b.shape:
        raise ValueError("Input arrays must have the same shape.")

    # Ensure all elements in the arrays are integers
    if not np.issubdtype(np_pose_a.dtype, np.integer) or not np.issubdtype(np_pose_b.dtype, np.integer):
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
        emd_distance = np.sum(np.abs(np_pose_a - np_pose_b))

        # Normalize the EMD value
        max_emd = max_emd_from_shape(action_space_shape)
        normmalized_emd = emd_distance / max_emd

        return normmalized_emd

    # Case 3: Dynamic distance (to be implemented)
    elif distance_type == "dynamic":
        trajectory_a = trajectory_array[tuple(np_pose_a)]
        trajectory_b = trajectory_array[tuple(np_pose_b)]

        dynamic_distance = dynamic_distance_calculator(trajectory_a, trajectory_b)

        if max_dynamic_distance is None:
            max_dynamic_distance = max_dynamic_distance_calculator(trajectory_array)  # Placeholder for future implementation

        normmalized_dynamic_distance = dynamic_distance / max_dynamic_distance

        return normmalized_dynamic_distance  # Placeholder for future implementation


    else:
        raise ValueError("Invalid distance_type. Choose from 'none', 'emd', or 'dynamic'.")



# Example usage
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "test":

    test_action_space_shape = (2, 3, 3, 3, 2, 3)

    np_pose_a = np.array([1, 2, 2, 2, 1, 2])
    np_pose_b = np.array([0, 0, 0, 0, 0, 0])

    print("Input arrays:")
    print("np_pose_a shape", np_pose_a.shape)
    print("np_pose_b shape", np_pose_b.shape)

    print("None distance:", calculate_distance(distance_type="none", np_pose_a=np_pose_a, np_pose_b=np_pose_b))  
    print("EMD distance:", calculate_distance(distance_type="emd", np_pose_a=np_pose_a, np_pose_b=np_pose_b, action_space_shape=test_action_space_shape))
    print("Dynamic distance:", calculate_distance(distance_type="dynamic", np_pose_a=np_pose_a, np_pose_b=np_pose_b))  # Placeholder



