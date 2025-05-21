// server/index.js

import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import bodyParser from 'body-parser';
import { OpenAIClient, AzureKeyCredential } from '@azure/openai';

dotenv.config();
const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(bodyParser.json());

// Configuración de Azure OpenAI
const endpoint = process.env.AZURE_OPENAI_ENDPOINT;
const apiKey = process.env.AZURE_OPENAI_KEY;
const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT;

const client = new OpenAIClient(endpoint, new AzureKeyCredential(apiKey));

app.post('/api/generar', async (req, res) => {
  const { prompt, tono, audiencia } = req.body;

  const systemMessage = `Eres un redactor oficial del departamento de prensa de un organismo estatal. 
Redacta el contenido solicitado con tono ${tono}, dirigido al ${audiencia}. 
Asegúrate de que el mensaje sea claro, institucional, empático y socialmente responsable.`;

  try {
    const response = await client.getChatCompletions(deploymentName, [
      { role: 'system', content: systemMessage },
      { role: 'user', content: prompt }
    ], {
      temperature: 0.7,
      maxTokens: 800
    });

    const texto = response.choices[0]?.message?.content;
    res.json({ texto });

  } catch (error) {
    console.error('Error en Azure OpenAI:', error);
    res.status(500).json({ error: 'Error al generar contenido' });
  }
});

app.listen(port, () => {
  console.log(`🚀 Servidor backend escuchando en http://localhost:${port}`);
});
