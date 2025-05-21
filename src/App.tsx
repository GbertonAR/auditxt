// src/App.tsx
import React from 'react';
import RedactorForm from '../redator-prensa/src/components/RedactorForm';

export default function App() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Redactor Prensa</h1>
      <RedactorForm />
    </div>
  );
}
