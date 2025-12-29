# 🏠 Gerenciador de Tarefas Domésticas - WEB

Sistema completo para monitorar e gerenciar tarefas simples do dia a dia da casa. **Versão Web** para acesso de toda a família em qualquer dispositivo (PC, tablet, celular).

## 📋 Funcionalidades

- ✅ Cadastro de tarefas com data e categoria
- 🔔 Alertas automáticos para tarefas próximas do vencimento
- 🔄 Repetição automática de tarefas (mensal, anual, trimestral, etc.)
- 📊 Visualização organizada por data com código de cores
- ✏️ Edição e exclusão de tarefas
- 💾 Salvamento automático em arquivo JSON
- 🌐 **Interface Web responsiva** - funciona em qualquer dispositivo
- 👨‍👩‍👧‍👦 **Acesso compartilhado** - toda a família pode acessar
- 📱 **Mobile-friendly** - otimizado para celulares

## 🎯 Categorias Disponíveis

- 🎂 Aniversário
- 🔥 Troca de Gás
- 🐕 Vacinação Pet
- 💰 Contas
- 🔧 Manutenção Casa
- 🛒 Compras
- 📝 Outro

## 🚀 Como Usar

### Instalação

1. Certifique-se de ter Python instalado (versão 3.6 ou superior)
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

### Executar o Servidor

```bash
python app.py
```

O servidor iniciará em: `http://0.0.0.0:5000`

### Acessar de Outros Dispositivos

1. No computador que está rodando o servidor, descubra o IP:
   - Windows: `ipconfig` (procure por "Endereço IPv4")
   - Linux/Mac: `ifconfig` ou `ip addr`

2. Em outros dispositivos na mesma rede Wi-Fi, acesse:
   ```
   http://SEU_IP:5000
   ```
   Exemplo: `http://192.168.1.100:5000`

3. **Dica**: Salve como favorito nos celulares da família!


### Adicionar uma Tarefa

1. Preencha a **Descrição** da tarefa
2. Selecione a **Categoria**
3. Informe a **Data**
4. Escolha se a tarefa deve **Repetir** (opcional)
5. Clique em **Adicionar Tarefa**

### Gerenciar Tarefas

- **✓ Marcar como Concluída**: Clique no botão verde. Se for uma tarefa recorrente, ela será automaticamente reagendada.
- **✏️ Editar**: Clique no botão amarelo para modificar os dados.
- **🗑️ Excluir**: Clique no botão vermelho para remover a tarefa.
- **📋 Histórico**: Acesse o histórico para ver todas as tarefas concluídas.

## 🎨 Sistema de Cores

- 🔴 **Vermelho**: Tarefas atrasadas ou para hoje
- 🟡 **Amarelo**: Tarefas na próxima semana ou no mês atual
- 🟢 **Verde**: Tarefas em dia (mais de 30 dias)

## ⚠️ Alertas

O sistema exibe alertas na parte superior da janela para:
- Tarefas atrasadas
- Tarefas para hoje
- Tarefas nos próximos 3 dias

## 💾 Armazenamento de Dados

As tarefas são salvas automaticamente no arquivo `tarefas_casa.json` no mesmo diretório do programa.


## 📝 Exemplos de Uso

### Exemplo 1: Aniversário
- **Descrição**: Aniversário da Maria
- **Categoria**: Aniversário
- **Data**: 15/03/2026
- **Repetir**: Anual

### Exemplo 2: Troca de Gás
- **Descrição**: Trocar botijão de gás
- **Categoria**: Troca de Gás
- **Data**: 05/01/2026
- **Repetir**: A cada 3 meses

### Exemplo 3: Vacinação do Pet
- **Descrição**: Vacina antirrábica - Rex
- **Categoria**: Vacinação Pet
- **Data**: 20/02/2026
- **Repetir**: Anual

## 🔄 Tipos de Repetição

- **Não repetir**: Tarefa única
- **Mensal**: Repete a cada 30 dias
- **Anual**: Repete no mesmo dia do próximo ano
- **A cada 3 meses**: Repete a cada 90 dias
- **A cada 6 meses**: Repete a cada 180 dias

## 🛠️ Requisitos do Sistema

- Python 3.6+
- Flask 3.0.0
- Navegador web moderno
- Conexão na mesma rede Wi-Fi (para acesso de outros dispositivos)

## 🌐 Recursos da Interface Web

- **Design Responsivo**: Adapta-se automaticamente a qualquer tamanho de tela
- **Interface Moderna**: Design com gradientes e animações suaves
- **Códigos de Cor**: 
  - 🔴 Vermelho: Tarefas atrasadas ou para hoje
  - 🟡 Amarelo: Tarefas na próxima semana ou no mês atual
  - 🟢 Verde: Tarefas em dia (mais de 30 dias)
- **Alertas Visuais**: Notificações destacadas no topo da página
- **Histórico**: Página separada para visualizar tarefas concluídas

## 🔒 Dicas de Segurança

- O servidor roda na rede local (não é acessível pela internet)
- Mantenha o computador que hospeda o servidor sempre ligado
- Para acesso externo, considere usar serviços como ngrok (avançado)

## 📱 Acessando no Celular

1. Certifique-se de que o celular está na mesma rede Wi-Fi
2. Abra o navegador (Chrome, Safari, etc.)
3. Digite o endereço: `http://IP_DO_COMPUTADOR:5000`
4. Salve nos favoritos para acesso rápido!

## 🚨 Solução de Problemas

### Não consigo acessar de outro dispositivo
- Verifique se ambos os dispositivos estão na mesma rede Wi-Fi
- Confirme o IP do computador com `ipconfig`
- Desative temporariamente o firewall para testar

### O servidor não inicia
- Verifique se a porta 5000 não está em uso
- Execute: `pip install -r requirements.txt` novamente
- Verifique se há erros no terminal

## 📧 Suporte

Para dúvidas ou sugestões, basta modificar o código conforme suas necessidades!

---

**Desenvolvido para simplificar o gerenciamento das tarefas domésticas da família! 🏡👨‍👩‍👧‍👦**
