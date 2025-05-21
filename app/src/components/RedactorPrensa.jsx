import React, { useState } from 'react';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Select, SelectTrigger, SelectContent, SelectItem } from '@/components/ui/select';

export default function GeneradorComunicado() {
  const [tipo, setTipo] = useState('comunicado de prensa');
  const [tono, setTono] = useState('formal');
  const [audiencia, setAudiencia] = useState('general');
  const [prompt, setPrompt] = useState('');
  const [resultado, setResultado] = useState('');
  const [editado, setEditado] = useState('');
  const [versiones, setVersiones] = useState([]);

  const generar = async () => {
    const response = await fetch('/api/generar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tipo, tono, audiencia, prompt })
    });
    const data = await response.json();
    setResultado(data.resultado);
    setEditado(data.resultado);
    setVersiones([...versiones, data.resultado]);
  };

  const guardar = () => {
    const blob = new Blob([editado], { type: 'text/plain;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `comunicado_${Date.now()}.txt`;
    link.click();
  };

  return (
    <div className="p-6 space-y-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold">Generador de Contenidos para Prensa</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Select onValueChange={setTipo} defaultValue={tipo}>
          <SelectTrigger>Tipo: {tipo}</SelectTrigger>
          <SelectContent>
            <SelectItem value="comunicado de prensa">Comunicado de Prensa</SelectItem>
            <SelectItem value="correo institucional">Correo Institucional</SelectItem>
            <SelectItem value="post de redes">Post de Redes Sociales</SelectItem>
            <SelectItem value="boletín interno">Boletín Interno</SelectItem>
          </SelectContent>
        </Select>

        <Select onValueChange={setTono} defaultValue={tono}>
          <SelectTrigger>Tono: {tono}</SelectTrigger>
          <SelectContent>
            <SelectItem value="formal">Formal</SelectItem>
            <SelectItem value="amigable">Amigable</SelectItem>
            <SelectItem value="técnico">Técnico</SelectItem>
          </SelectContent>
        </Select>

        <Select onValueChange={setAudiencia} defaultValue={audiencia}>
          <SelectTrigger>Audiencia: {audiencia}</SelectTrigger>
          <SelectContent>
            <SelectItem value="general">General</SelectItem>
            <SelectItem value="interna">Interna</SelectItem>
            <SelectItem value="institucional">Institucional</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Textarea
        className="w-full min-h-[80px]"
        placeholder="Describe el contenido que deseas generar..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <Button onClick={generar}>Generar Contenido</Button>

      {resultado && (
        <Card className="mt-4">
          <CardContent className="space-y-4">
            <h2 className="text-xl font-semibold">Vista Previa (editable)</h2>
            <Textarea
              className="w-full min-h-[200px]"
              value={editado}
              onChange={(e) => setEditado(e.target.value)}
            />
            <Button onClick={guardar}>Guardar</Button>
          </CardContent>
        </Card>
      )}

      {versiones.length > 1 && (
        <div className="mt-6">
          <h3 className="font-bold">Versiones Generadas:</h3>
          <ul className="list-disc pl-6 space-y-2">
            {versiones.map((v, i) => (
              <li key={i} className="text-sm truncate">Versión {i + 1}: {v.slice(0, 80)}...</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
