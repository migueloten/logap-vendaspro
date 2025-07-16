# Desafio Vogal - API

## O que faz
Encontra a primeira vogal que aparece depois de uma consoante, sendo que essa consoante tem uma vogal antes dela. A vogal encontrada não pode se repetir na string.

## Regras simples
- Procura o padrão: **vogal → consoante → vogal**
- A vogal final não pode aparecer mais vezes na string
- Só usa código Python nativo

## Como usar

**Enviar string:**
```bash
curl -X POST "http://localhost:8000/api/v1/desafio-vogal/processar/" \
  -H "Content-Type: application/json" \
  -d '{"string": "aAbBABacafe"}'
```

**Resposta:**
```json
{
  "string": "aAbBABacafe",
  "vogal": "e",
  "tempoTotal": "0.16ms"
}
```

## Exemplo prático

Na string `"aAbBABacafe"`:
- Encontra `a-f-e` nas posições 8, 9, 10
- O `e` não se repete na string inteira
- Resultado: `e`

## Endpoints

- `POST /api/v1/desafio-vogal/processar/` - Processa a string
- `GET /api/v1/desafio-vogal/exemplo/` - Mostra exemplo de uso

## Características
- Complexidade O(n) - eficiente
- Mede tempo de processamento
