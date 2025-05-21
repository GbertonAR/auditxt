import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";

export function RedactorForm() {
  const [tipo, setTipo] = useState("comunicado");
  const [tono, setTono] = useState("formal");
  const [audiencia, setAudiencia] = useState("general");
  const [prompt, setPrompt] = useState("");
  const [resultado, setResultado] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setResultado("");
    setLoading(true);

    try {
      const res = await fetch("/api/generar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ tipo, tono, audiencia, prompt }),
      });

      if (!res.ok) throw new Error("Error al generar contenido");

      const data = await res.json();
      setResultado(data.resultado || "No se recibió respuesta.");
    } catch (err) {
      console.error(err);
      setResultado("❌ Error al generar el contenido.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-2xl shadow-md w-full max-w-2xl space-y-4">
      <h2 className="text-xl font-bold">Generador de Contenido de Prensa</h2>

      <div>
        <Label>Tipo de contenido</Label>
        <Select value={tipo} onValueChange={setTipo}>
          <SelectTrigger>
            <SelectValue placeholder="Seleccionar tipo" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="comunicado">Comunicado de prensa</SelectItem>
            <SelectItem value="correo">Correo institucional</SelectItem>
            <SelectItem value="post">Post para redes sociales</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div>
        <Label>Tono</Label>
        <Select value={tono} onValueChange={setTono}>
          <SelectTrigger>
            <SelectValue placeholder="Seleccionar tono" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="formal">Formal</SelectItem>
            <SelectItem value="amigable">Amigable</SelectItem>
            <SelectItem value="técnico">Técnico</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div>
        <Label>Audiencia</Label>
        <Select value={audiencia} onValueChange={setAudiencia}>
          <SelectTrigger>
            <SelectValue placeholder="Seleccionar audiencia" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="general">Público general</SelectItem>
            <SelectItem value="interna">Audiencia interna</SelectItem>
            <SelectItem value="institucional">Institucional</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div>
        <Label>¿Qué contenido querés generar?</Label>
        <Textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describí brevemente el contenido que necesitás..."
          rows={4}
          required
        />
      </div>

      <Button type="submit" disabled={loading}>
        {loading ? "Generando..." : "Generar"}
      </Button>

      {/* {resultado && (
        <div className="mt-4">
          <Label>Resultado generado:</Label>
          <Textarea className="mt-2" value={resultado} rows={10} readOnly />
        </div>
      )} */}

      {resultado && (
        <div className="mt-4 p-4 bg-white border rounded max-h-60 overflow-auto whitespace-pre-wrap">
            <h3 className="font-semibold mb-2">Resultado generado:</h3>
            <pre>{resultado}</pre>
        </div>
    )}
    </form>
  );
}
