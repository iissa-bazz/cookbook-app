import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Modal({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();
  
  // Handle Escape key
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        navigate('/');
      }
    };
    // Add listener when component mounts
    window.addEventListener('keydown', handleKeyDown);
    document.body.style.overflow = 'hidden'; // Stop background scroll
    // Clean up listener when component unmounts
    return () =>  {
        window.removeEventListener('keydown', handleKeyDown) ;
        document.body.style.overflow = 'unset'; // Restore scroll on close
    };
  }, [navigate]); // 


  return (
    <div style={overlayStyle} onClick={() => navigate('/')}>
      <div style={modalStyle} onClick={(e) => e.stopPropagation()}>
        <button onClick={() => navigate('/')} style={{ backgroundColor: 'rgba(181, 199, 220, 0.69)', float: 'right' }}>Close</button>
        {children}
      </div>
    </div>
  );
}

const overlayStyle: React.CSSProperties = {
  position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh',
  backgroundColor: 'rgba(132, 152, 175, 0.69)', display: 'flex', justifyContent: 'center', alignItems: 'center'
};

const modalStyle: React.CSSProperties = {
  background: 'rgba(250, 244, 227, 1)', padding: '2rem', borderRadius: '8px', minWidth: '400px', maxWidth: '90%'
};