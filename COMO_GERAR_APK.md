# Como gerar o APK do WS Alimentação (Android)

O APK é compilado **de graça nos servidores do GitHub** (GitHub Actions) — não
precisa instalar nada no seu PC. Ao final você baixa o `.apk` e instala no
celular. É o mesmo app da versão web, dentro de um aplicativo Android, com PDF e
Excel salvos na pasta **Download** do aparelho.

> Por que não gerar aqui? Compilar Android exige baixar o SDK/NDK do Google
> (vários GB), o que só roda com internet liberada — por isso usamos o GitHub.

---

## Passo a passo

### 1. Crie um repositório novo (separado do site)
- Em https://github.com/new, nome: **`ws-alimentacao-apk`** → **Create repository**.
  (Use um repositório **só para o APK**, diferente do `ws-alimentacao` do site.)

### 2. Envie os arquivos do projeto
- Na página do repositório vazio, clique em **uploading an existing file**.
- Abra a pasta `WSApk` (a que veio no zip), selecione **tudo que está dentro**
  (`main.py`, `buildozer.spec`, `icon.png`, a pasta `webapp`) e arraste para a
  área de upload. Clique em **Commit changes**.

### 3. Crie o arquivo do build (importante!)
A pasta `.github` costuma não subir pelo arrastar. Crie-a pelo site:
- Clique em **Add file → Create new file**.
- No campo do nome, digite exatamente:
  `.github/workflows/android-build.yml`
  (ao digitar as barras `/`, o GitHub cria as pastas sozinho).
- Cole **todo o conteúdo** do arquivo `.github/workflows/android-build.yml` que
  está no zip (abra com o Bloco de Notas e copie), e clique em **Commit changes**.

### 4. Aguarde a compilação
- Vá na aba **Actions**. O build **"Gerar APK Android"** começa sozinho.
- A **primeira compilação leva ~20 minutos**. Quando ficar com o ✔️ verde, terminou.

### 5. Baixe o APK
Duas formas:
- **Release (recomendado):** na página inicial do repositório, no lado direito em
  **Releases**, abra **WS Alimentação — APK** e baixe o arquivo `.apk`.
  Esse link é permanente — dá para abrir direto no navegador do celular.
- **Artefato:** na aba **Actions**, abra a execução concluída, role até
  **Artifacts** e baixe **WS-Alimentacao-APK** (vem num .zip).

### 6. Instale no celular
1. Passe o `.apk` para o celular (ou baixe direto pelo link do Release).
2. Ao tocar no arquivo, o Android pedirá para permitir **"instalar apps
   desconhecidos"** para o app que está abrindo (Arquivos ou navegador) —
   autorize.
3. Toque em **Instalar**. Pronto, o WS Alimentação aparece na sua lista de apps.

> O APK é "debug" (assinatura de teste) — normal para uso pessoal/interno.
> O Android pode mostrar um aviso do Play Protect; toque em "Instalar mesmo assim".

---

## Observações
- **Dados:** ficam salvos dentro do app, no celular. Use a tela **Backup** para
  baixar/restaurar um `.json` e levar os dados para outro aparelho.
- **Atualizar o app:** se eu te mandar uma versão nova, basta substituir os
  arquivos no repositório (Commit) que o GitHub recompila e gera um APK novo.
- **Ícone e nome:** já vêm com o logo e o nome "WS Alimentação".
