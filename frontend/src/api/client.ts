import axios from 'axios';
import  type  { RecipeSuggestion, SuggestionRequest } from '../types';
// ... existing imports
import type { Instruction } from '../types';

export const queryKeys = {
  recipes: {
    suggestions: (req: any) => ['recipes', 'suggestions', req] as const,
    instructions: () => ['recipes', 'instructions'] as const, // Key for all instructions
  },
};

//export const queryKeys = {
//  recipes: {
//    suggestions: (req: SuggestionRequest) => ['recipes', 'suggestions', req] as const,
//    detail: (name: string) => ['recipes', 'detail', name] as const,
//  },
//};

const apiClient = axios.create({
    baseURL: '/api', 
    headers: { 'Content-Type': 'application/json' },
});

export const fetchSuggestions = async (req: SuggestionRequest): Promise<RecipeSuggestion[]> => {
    const response = await apiClient.post<RecipeSuggestion[]>(`/recipes/suggestions`, req);
    return response.data;
};

export const fetchInstructions = async (): Promise<Instruction[]> => {
  const response = await apiClient.get<Instruction[]>(`/instructions`);
  return response.data;
};

export default apiClient;