from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime, timedelta
from functools import wraps
import json
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-mude-em-producao'

ARQUIVO_DADOS = 'tarefas_casa.json'

# Credenciais (em produção, use hash de senha e banco de dados)
USUARIOS = {
    'admin': '123password'
}


def login_required(f):
    """Decorator para proteger rotas que precisam de autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def carregar_tarefas():
    """Carrega as tarefas do arquivo JSON"""
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo JSON"""
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)


def calcular_status_tarefa(data_str):
    """Calcula o status e dias restantes de uma tarefa"""
    data_tarefa = datetime.strptime(data_str, "%Y-%m-%d")
    hoje = datetime.now()
    dias_restantes = (data_tarefa - hoje).days
    
    if dias_restantes < 0:
        status = "ATRASADA"
        cor = "danger"
        icone = "⚠️"
    elif dias_restantes == 0:
        status = "HOJE"
        cor = "danger"
        icone = "🔔"
    elif dias_restantes <= 3:
        status = "URGENTE"
        cor = "warning"
        icone = "🔥"
    elif dias_restantes <= 7:
        status = "Esta semana"
        cor = "warning"
        icone = "⏰"
    elif dias_restantes <= 30:
        status = "Este mês"
        cor = "info"
        icone = "📅"
    else:
        status = "Em dia"
        cor = "success"
        icone = "✓"
    
    return {
        'dias_restantes': dias_restantes,
        'status': status,
        'cor': cor,
        'icone': icone
    }


def obter_alertas(tarefas):
    """Retorna lista de alertas para tarefas urgentes"""
    alertas = []
    hoje = datetime.now()
    
    for tarefa in tarefas:
        if tarefa.get('concluida'):
            continue
        
        data_tarefa = datetime.strptime(tarefa['data'], "%Y-%m-%d")
        dias_restantes = (data_tarefa - hoje).days
        
        if dias_restantes < 0:
            alertas.append({
                'tipo': 'danger',
                'mensagem': f"{tarefa['nome']} está ATRASADA!",
                'icone': '🔴'
            })
        elif dias_restantes == 0:
            alertas.append({
                'tipo': 'danger',
                'mensagem': f"{tarefa['nome']} é HOJE!",
                'icone': '🔴'
            })
        elif dias_restantes <= 3:
            alertas.append({
                'tipo': 'warning',
                'mensagem': f"{tarefa['nome']} em {dias_restantes} dias",
                'icone': '🟡'
            })
    
    return alertas


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        senha = request.form.get('senha', '').strip()
        
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro='Usuário ou senha incorretos!')
    
    # Se já está logado, redireciona para o index
    if 'usuario' in session:
        return redirect(url_for('index'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Faz logout do usuário"""
    session.pop('usuario', None)
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    """Página principal"""
    tarefas = carregar_tarefas()
    
    # Filtrar tarefas não concluídas e adicionar informações de status
    tarefas_ativas = []
    for tarefa in tarefas:
        if not tarefa.get('concluida'):
            info_status = calcular_status_tarefa(tarefa['data'])
            tarefa_com_status = tarefa.copy()
            tarefa_com_status.update(info_status)
            
            # Formatar data para exibição
            data_obj = datetime.strptime(tarefa['data'], "%Y-%m-%d")
            tarefa_com_status['data_formatada'] = data_obj.strftime("%d/%m/%Y")
            
            tarefas_ativas.append(tarefa_com_status)
    
    # Ordenar por data
    tarefas_ativas.sort(key=lambda x: x['data'])
    
    # Obter alertas
    alertas = obter_alertas(tarefas)
    
    return render_template('index.html', 
                         tarefas=tarefas_ativas, 
                         alertas=alertas,
                         total_tarefas=len(tarefas_ativas))


@app.route('/adicionar', methods=['POST'])
@login_required
def adicionar_tarefa():
    """Adiciona uma nova tarefa"""
    try:
        nome = request.form.get('nome', '').strip()
        categoria = request.form.get('categoria', 'Outro')
        data_str = request.form.get('data', '').strip()
        repeticao = request.form.get('repeticao', 'Não repetir')
        
        if not nome or not data_str:
            return jsonify({'erro': 'Preencha todos os campos obrigatórios'}), 400
        
        # Validar e converter data
        try:
            data_obj = datetime.strptime(data_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({'erro': 'Data inválida'}), 400
        
        # Se for uma tarefa recorrente e a data está no passado, calcular a próxima ocorrência
        hoje = datetime.now()
        if repeticao != 'Não repetir' and data_obj < hoje:
            while data_obj < hoje:
                if repeticao == 'Mensal':
                    data_obj = data_obj + timedelta(days=30)
                elif repeticao == 'Anual':
                    try:
                        data_obj = data_obj.replace(year=data_obj.year + 1)
                    except ValueError:
                        data_obj = data_obj.replace(year=data_obj.year + 1, day=28)
                elif repeticao == 'A cada 3 meses':
                    data_obj = data_obj + timedelta(days=90)
                elif repeticao == 'A cada 6 meses':
                    data_obj = data_obj + timedelta(days=180)
        
        tarefas = carregar_tarefas()
        
        nova_tarefa = {
            'id': max([t.get('id', 0) for t in tarefas], default=0) + 1,
            'nome': nome,
            'categoria': categoria,
            'data': data_obj.strftime("%Y-%m-%d"),
            'repeticao': repeticao,
            'concluida': False
        }
        
        tarefas.append(nova_tarefa)
        salvar_tarefas(tarefas)
        
        return jsonify({'sucesso': True, 'mensagem': 'Tarefa adicionada com sucesso!'})
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/concluir/<int:tarefa_id>', methods=['POST'])
@login_required
def concluir_tarefa(tarefa_id):
    """Marca uma tarefa como concluída ou a reagenda se for recorrente"""
    try:
        tarefas = carregar_tarefas()
        
        for tarefa in tarefas:
            if tarefa['id'] == tarefa_id and not tarefa.get('concluida'):
                # Verificar se deve repetir
                if tarefa['repeticao'] != 'Não repetir':
                    data_atual = datetime.strptime(tarefa['data'], "%Y-%m-%d")
                    hoje = datetime.now()
                    
                    # Calcular próxima data a partir da data atual da tarefa
                    if tarefa['repeticao'] == 'Mensal':
                        nova_data = data_atual + timedelta(days=30)
                    elif tarefa['repeticao'] == 'Anual':
                        try:
                            nova_data = data_atual.replace(year=data_atual.year + 1)
                        except ValueError:
                            # Para 29 de fevereiro em anos não bissextos
                            nova_data = data_atual.replace(year=data_atual.year + 1, day=28)
                    elif tarefa['repeticao'] == 'A cada 3 meses':
                        nova_data = data_atual + timedelta(days=90)
                    elif tarefa['repeticao'] == 'A cada 6 meses':
                        nova_data = data_atual + timedelta(days=180)
                    else:
                        nova_data = data_atual
                    
                    # Se a nova data calculada ainda é no passado, continuar somando períodos até estar no futuro
                    while nova_data < hoje:
                        if tarefa['repeticao'] == 'Mensal':
                            nova_data = nova_data + timedelta(days=30)
                        elif tarefa['repeticao'] == 'Anual':
                            try:
                                nova_data = nova_data.replace(year=nova_data.year + 1)
                            except ValueError:
                                nova_data = nova_data.replace(year=nova_data.year + 1, day=28)
                        elif tarefa['repeticao'] == 'A cada 3 meses':
                            nova_data = nova_data + timedelta(days=90)
                        elif tarefa['repeticao'] == 'A cada 6 meses':
                            nova_data = nova_data + timedelta(days=180)
                    
                    tarefa['data'] = nova_data.strftime("%Y-%m-%d")
                    mensagem = f"Tarefa reagendada para {nova_data.strftime('%d/%m/%Y')}"
                else:
                    tarefa['concluida'] = True
                    mensagem = "Tarefa marcada como concluída!"
                
                salvar_tarefas(tarefas)
                return jsonify({'sucesso': True, 'mensagem': mensagem})
        
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/excluir/<int:tarefa_id>', methods=['POST'])
@login_required
def excluir_tarefa(tarefa_id):
    """Exclui uma tarefa"""
    try:
        tarefas = carregar_tarefas()
        tarefas_filtradas = [t for t in tarefas if t['id'] != tarefa_id]
        
        if len(tarefas_filtradas) == len(tarefas):
            return jsonify({'erro': 'Tarefa não encontrada'}), 404
        
        salvar_tarefas(tarefas_filtradas)
        return jsonify({'sucesso': True, 'mensagem': 'Tarefa excluída com sucesso!'})
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/editar/<int:tarefa_id>', methods=['GET', 'POST'])
@login_required
def editar_tarefa(tarefa_id):
    """Edita uma tarefa existente"""
    tarefas = carregar_tarefas()
    
    if request.method == 'GET':
        # Buscar tarefa para edição
        for tarefa in tarefas:
            if tarefa['id'] == tarefa_id:
                return jsonify(tarefa)
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    
    elif request.method == 'POST':
        try:
            nome = request.form.get('nome', '').strip()
            categoria = request.form.get('categoria', 'Outro')
            data_str = request.form.get('data', '').strip()
            repeticao = request.form.get('repeticao', 'Não repetir')
            
            if not nome or not data_str:
                return jsonify({'erro': 'Preencha todos os campos obrigatórios'}), 400
            
            # Validar data
            try:
                data_obj = datetime.strptime(data_str, "%Y-%m-%d")
            except ValueError:
                return jsonify({'erro': 'Data inválida'}), 400
            
            # Atualizar tarefa
            for tarefa in tarefas:
                if tarefa['id'] == tarefa_id:
                    tarefa['nome'] = nome
                    tarefa['categoria'] = categoria
                    tarefa['data'] = data_obj.strftime("%Y-%m-%d")
                    tarefa['repeticao'] = repeticao
                    
                    salvar_tarefas(tarefas)
                    return jsonify({'sucesso': True, 'mensagem': 'Tarefa atualizada com sucesso!'})
            
            return jsonify({'erro': 'Tarefa não encontrada'}), 404
        
        except Exception as e:
            return jsonify({'erro': str(e)}), 500


@app.route('/historico')
@login_required
def historico():
    """Página com histórico de tarefas concluídas"""
    tarefas = carregar_tarefas()
    tarefas_concluidas = [t for t in tarefas if t.get('concluida')]
    
    # Adicionar data formatada
    for tarefa in tarefas_concluidas:
        data_obj = datetime.strptime(tarefa['data'], "%Y-%m-%d")
        tarefa['data_formatada'] = data_obj.strftime("%d/%m/%Y")
    
    # Ordenar por data (mais recentes primeiro)
    tarefas_concluidas.sort(key=lambda x: x['data'], reverse=True)
    
    return render_template('historico.html', tarefas=tarefas_concluidas)


if __name__ == "__main__":
    app.run(debug=True)  # só para uso local

