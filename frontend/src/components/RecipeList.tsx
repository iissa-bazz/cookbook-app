import { useQuery } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { fetchSuggestions, queryKeys } from '../api/client';
import type { SuggestionRequest } from '../types';
import { Outlet, Link } from 'react-router-dom';

export default function RecipeListPage() {
  // 1. Form setup for Portions and Scope
  const { register, watch } = useForm<SuggestionRequest>({
    defaultValues: { portions: 4, scope: 14 }
  });

  // watch values to make the query reactive
  const currentParams = watch();

  // fetch data based on form state
  const { data: suggestions, isLoading, isError } = useQuery({
    queryKey: queryKeys.recipes.suggestions(currentParams),
    queryFn: () => fetchSuggestions(currentParams),
    placeholderData: (previousData) => previousData, // smooth transition between updates
  });

  return (
    <div style={{ padding: '20px' }}>
      <h1>Recipe Suggestions</h1>

      {/* Inputs Section */}
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px', background: '#f4f4f4', padding: '15px', borderRadius: '8px' }}>
        <label>
          <strong>Portions:</strong>
          <input type="number" {...register("portions", { valueAsNumber: true })} style={inputStyle} />
        </label>
        <label>
          <strong>Expiration Scope (Days):</strong>
          <input type="number" {...register("scope", { valueAsNumber: true })} style={inputStyle} />
        </label>
      </div>

      {isLoading && !suggestions ? (
        <div>Loading delicious suggestions...</div>
      ) : (
        <table className="recipe-table" style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #ddd' }}>
              <th>Recipe</th>
              <th>Missing</th>
              <th>Expiring Soon</th>
              <th>Price/Portion</th>
              <th>Total Cost</th>
            </tr>
          </thead>
          <tbody>
            {suggestions?.map((r) => (
              <tr key={r.recipe} style={{ borderBottom: '1px solid #eee' }}>
                <td>
                  <Link to={`/recipes/${encodeURIComponent(r.recipe)}`}><strong>{r.recipe}</strong></Link>
                </td>
                <td style={{ color: r.missing_ingredients > 0 ? '#cd6143b7' : 'lightgreen' }}>
                   {r.missing_ingredients} / {r.nbr_of_ingredients}
                </td>
                <td title={r.expiring_ingredients}>
                   {r.expiring_within_scope} items
                </td>
                <td>CHF {r.price_per_portion.toFixed(2)}</td>
                <td><strong>CHF {r.cost.toFixed(2)}</strong></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* this renders the Details Modal when a recipe is clicked */}
      <Outlet />
    </div>
  );
}

const inputStyle = { marginLeft: '10px', padding: '5px', width: '60px' };