# resolvedor-py

## Como Rodar

### Servidor Python
Com Python 3.10+ instalado, na raiz do projeto rode:

```bash
python -m venv venv
source venv/bin/activate
cd server/
pip install -r requirements.txt
python app.py
```

### Frontend Svelte
Com Nodejs 22+ instalado, na raiz do projeto rode:

```bash
cd webapp/
npm install
npm run dev
```

É necessário criar um arquivo .env dentro da pasta ```server/``` contendo as variáveis de ambiente da chave de API do Gemini e a URI do banco de dados MongoDB:
```
GEMINI_API_KEY=<sua chave>
MONGODB_URI=<sua_uri_mongodb_atlas>
```
