/**
 * Custom hook for assessment functionality
 */
import { useState } from 'react';
import { assessmentAPI } from '../services/api';

export const useAssessment = () => {
  const [state, setState] = useState({
    isLoading: false,
    results: null,
    error: null,
  });

  const analyze = async (text) => {
    setState({ isLoading: true, results: null, error: null });

    try {
      const response = await assessmentAPI.analyze(text);
      setState({ isLoading: false, results: response.data, error: null });
      return response.data;
    } catch (error) {
      const errorMessage =
        error.response?.data?.error?.message || error.message || 'An error occurred';
      setState({
        isLoading: false,
        results: null,
        error: errorMessage,
      });
      throw error;
    }
  };

  const reset = () => {
    setState({ isLoading: false, results: null, error: null });
  };

  return {
    isLoading: state.isLoading,
    results: state.results,
    error: state.error,
    analyze,
    reset,
  };
};
