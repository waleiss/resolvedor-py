# resolvedor-py

##Feedback
O módulo de feedback com LLM no avaliador foi implementado na API para automaticamente dar um feedback para o estudante a cada passo errado que ele apresentar para o sistema, e apenas se houver algum erro na solução dele.
- Por exemplo, para a seguinte solução o sistema vai dar feedback:

```
{
  "premises": [
    "P → Q",
    "¬Q"
  ],
  "conclusion": "¬P",
  "inferences": [
    "(1)  ¬P  Modus Ponens  1, 2"
  ]
}
```
- Enquanto que a seguinte solução, por estar correta, não acionará o módulo de feedback:

```
{
  "premises": [
    "P → Q",
    "P"
  ],
  "conclusion": "Q",
  "inferences": [
    "(1)  Q  Modus Ponens  1, 2"
  ]
}
```
