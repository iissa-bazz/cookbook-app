import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ErrorBoundary } from 'react-error-boundary';
import { ErrorFallback } from './components/ErrorFallback';
import RecipeListPage from './components/RecipeList';
// You can create a simple RecipeDetails component later
import RecipeDetails from './components/RecipeDetails'; 

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { throwOnError: true, retry: 1 },
    mutations: { throwOnError: true },
  },
});

function App() {
  return (
    <>
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<RecipeListPage />}>
               {/* Nested route opens inside the Modal in the RecipeDetails component */}
               <Route path="recipes/:name" element={<RecipeDetails />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </ErrorBoundary>
    </>
  );
}

export default App;