# Como obter a connection string no MongoDB Atlas (passo a passo para a gravação)

1. Crie uma conta em <https://www.mongodb.com/atlas> e um cluster gratuito (**M0**).
2. **Database Access** -> *Add New Database User*: crie um usuário e uma senha **sem caracteres especiais**
   (ou codifique-os na URL) e permissão de leitura/escrita.
3. **Network Access** -> *Add IP Address*: adicione o seu IP (para estudo, `0.0.0.0/0` libera todos;
   **nunca** faça isso em produção).
4. No cluster, clique em **Connect** -> **Drivers** -> **Python** e copie a string:
   ```text
   mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/?retryWrites=true&w=majority
   ```
5. Cole no `.env` trocando `<usuario>` e `<senha>`:
   ```env
   MONGO_URI=mongodb+srv://helpdesk_app:MinhaSenha123@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority
   MONGO_DB_NAME=helpdesk
   ```
6. Teste: `python testar_conexao.py`.

**Cuidados de segurança**
- A connection string contém a senha: trate como segredo. Nunca em prints de tela, nunca no Git.
- Se vazar, apague o usuário em *Database Access* e crie outro.

**Alternativa local (sem conta nenhuma)**
```powershell
docker run -d --name helpdesk-mongo -p 27017:27017 mongo:7
```
