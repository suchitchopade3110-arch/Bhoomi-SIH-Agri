import React from 'react';
import { Providers } from './providers';
import { AppRouter } from './router';

export const App: React.FC = () => {
  return (
    <Providers>
      <AppRouter />
    </Providers>
  );
};
