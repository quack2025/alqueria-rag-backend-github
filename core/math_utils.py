# core/math_utils.py
"""
Pure Python implementations of math functions to avoid numpy/sklearn dependencies
For Azure App Service compatibility
"""

import math
from typing import List, Tuple


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors using pure Python.
    
    Args:
        vec1: First vector as list of floats
        vec2: Second vector as list of floats
        
    Returns:
        Cosine similarity score between -1 and 1
    """
    if len(vec1) != len(vec2):
        raise ValueError(f"Vectors must have same length. Got {len(vec1)} and {len(vec2)}")
    
    # Calculate dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Calculate magnitudes
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    # Calculate cosine similarity
    similarity = dot_product / (magnitude1 * magnitude2)
    
    # Ensure result is between -1 and 1 (floating point errors)
    return max(-1.0, min(1.0, similarity))


def normalize_vector(vec: List[float]) -> List[float]:
    """
    Normalize a vector to unit length.
    
    Args:
        vec: Vector to normalize
        
    Returns:
        Normalized vector
    """
    magnitude = math.sqrt(sum(x * x for x in vec))
    if magnitude == 0:
        return vec
    return [x / magnitude for x in vec]


def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate Euclidean distance between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Euclidean distance
    """
    if len(vec1) != len(vec2):
        raise ValueError(f"Vectors must have same length. Got {len(vec1)} and {len(vec2)}")
    
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


def dot_product(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate dot product of two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Dot product
    """
    if len(vec1) != len(vec2):
        raise ValueError(f"Vectors must have same length. Got {len(vec1)} and {len(vec2)}")
    
    return sum(a * b for a, b in zip(vec1, vec2))


def vector_mean(vectors: List[List[float]]) -> List[float]:
    """
    Calculate the mean of multiple vectors.
    
    Args:
        vectors: List of vectors
        
    Returns:
        Mean vector
    """
    if not vectors:
        return []
    
    num_vectors = len(vectors)
    vector_length = len(vectors[0])
    
    # Initialize mean vector with zeros
    mean = [0.0] * vector_length
    
    # Sum all vectors
    for vector in vectors:
        if len(vector) != vector_length:
            raise ValueError("All vectors must have the same length")
        for i in range(vector_length):
            mean[i] += vector[i]
    
    # Divide by number of vectors
    return [x / num_vectors for x in mean]


def top_k_similar(
    query_vector: List[float],
    vectors: List[Tuple[str, List[float]]],
    k: int = 5
) -> List[Tuple[str, float]]:
    """
    Find top-k most similar vectors to query vector.
    
    Args:
        query_vector: Query vector
        vectors: List of (id, vector) tuples
        k: Number of top results to return
        
    Returns:
        List of (id, similarity_score) tuples, sorted by similarity
    """
    similarities = []
    
    for vec_id, vec in vectors:
        similarity = cosine_similarity(query_vector, vec)
        similarities.append((vec_id, similarity))
    
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities[:k]


# Test functions to ensure correctness
def _test_cosine_similarity():
    """Test cosine similarity implementation"""
    # Test identical vectors
    assert abs(cosine_similarity([1, 0], [1, 0]) - 1.0) < 1e-10
    
    # Test orthogonal vectors
    assert abs(cosine_similarity([1, 0], [0, 1]) - 0.0) < 1e-10
    
    # Test opposite vectors
    assert abs(cosine_similarity([1, 0], [-1, 0]) - (-1.0)) < 1e-10
    
    # Test arbitrary vectors
    v1 = [1, 2, 3]
    v2 = [2, 3, 4]
    # Expected: ~0.9925
    result = cosine_similarity(v1, v2)
    assert 0.99 < result < 1.0
    
    print("✅ Cosine similarity tests passed!")


if __name__ == "__main__":
    _test_cosine_similarity()
    print("✅ All math utils tests passed!")