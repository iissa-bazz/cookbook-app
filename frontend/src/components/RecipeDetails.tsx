import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import Modal from './Modal';
import { fetchInstructions, queryKeys } from '../api/client';

export default function RecipeDetails() {
  const { name } = useParams<{ name: string }>();
  const decodedName = decodeURIComponent(name || "");

  const { data: ingredients, isLoading } = useQuery({
    queryKey: queryKeys.recipes.instructions(),
    queryFn: fetchInstructions,
    // The "Magic" part: Filter the global list for just this recipe
    select: (allInstructions) => 
      allInstructions.filter(item => item.recipe === decodedName),
    staleTime: 1000 * 60 * 5, // Cache instructions for 5 minutes
  });

  return (
    <Modal>
      <div style={{ minWidth: '350px' }}>
        <h2 style={{ borderBottom: '2px solid #eee', paddingBottom: '10px' }}>
          {decodedName}
        </h2>

        {isLoading ? (
          <p>Loading ingredients...</p>
        ) : ingredients && ingredients.length > 0 ? (
          <>
            <h3>Ingredients</h3>
            <ul style={{ lineHeight: '1.8' }}>
              {ingredients.map((item) => (
                <li key={item.id}>
                  <strong>{item.quantity} {item.unit}</strong> {item.ingredient}
                </li>
              ))}
            </ul>
          </>
        ) : (
          <p>No ingredient details found for this recipe.</p>
        )}

        <div style={{ marginTop: '20px', textAlign: 'right' }}>
          <Link to="/" style={{ color: '#666', textDecoration: 'none' }}>
            ← Back to Suggestions
          </Link>
        </div>
      </div>
    </Modal>
  );
}