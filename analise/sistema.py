from entidades.interacao import Interacao
from entidades.plataforma import Plataforma
from entidades.usuario import Usuario
from entidades.conteudo import Conteudo

class SistemaAnaliseEngajamento:
    """
    Classe que representa o sistema de análise de engajamento de conteúdos.
    Atributos:
        - VERSAO_ANALISE (str): Versão do sistema de análise.
        - __plataformas_registradas (dict): Dicionário que armazena as plataformas registradas.
        - __conteudos_registrados (dict): Dicionário que armazena os conteúdos registrados.
        - __usuarios_registrados (dict): Dicionário que armazena os usuários registrados.
        - __proximo_id_plataforma (int): Próximo ID a ser atribuído a uma plataforma.
    Métodos:
        - __init__: Inicializa o sistema com dicionários vazios e um ID inicial para plataformas.
        - cadastrar_plataforma: Cadastra uma nova plataforma ou retorna a existente.
        - obter_plataforma: Obtém uma plataforma pelo nome.
        - listar_plataformas: Lista todas as plataformas registradas.
        - _carregar_interacoes_csv: Carrega interações de um arquivo CSV.
        - processar_interacoes_do_csv: Processa interações do CSV e registra usuários, conteúdos e interações.
        - gerar_relatorio_engajamento_conteudos: Gera um relatório de engajamento dos conteúdos.
        - gerar_relatorio_atividade_usuarios: Gera um relatório de atividade dos usuários.
        - identificar_top_conteudos: Identifica os top conteúdos com base em uma métrica específica.
    """
    VERSAO_ANALISE = "2.0"

    def __init__(self):
        self.__plataformas_registradas = {}
        self.__conteudos_registrados = {}
        self.__usuarios_registrados = {}
        self.__proximo_id_plataforma = 1

    def cadastrar_plataforma(self, nome_plataforma):
        if nome_plataforma in self.__plataformas_registradas:
            return self.__plataformas_registradas[nome_plataforma]
        plataforma = Plataforma(nome_plataforma, id_plataforma=self.__proximo_id_plataforma)
        self.__plataformas_registradas[nome_plataforma] = plataforma
        self.__proximo_id_plataforma += 1
        return plataforma

    def obter_plataforma(self, nome_plataforma):
        return self.__plataformas_registradas.get(nome_plataforma)

    def listar_plataformas(self):
        return list(self.__plataformas_registradas.values())
    
    def _carregar_interacoes_csv(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()
                dados_brutos = [linha.strip().split(',') for linha in linhas]
                return dados_brutos
        except FileNotFoundError:
            print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
            return []
    
    def processar_interacoes_do_csv(self, caminho_arquivo):
        dados_brutos = self._carregar_interacoes_csv(caminho_arquivo)
        cabecalho = ['id_usuario', 'nome_conteudo', 'id_conteudo', 'timestamp_interacao', 'nome_plataforma', 'tipo_interacao', 'watch_duration_seconds', 'comment_text']
        for linha in dados_brutos[1:]:  # Ignora o cabeçalho
            try:
                dados = dict(zip(cabecalho, linha))
                usuario_id = int(dados['id_usuario'])
                timestamp_interacao = dados['timestamp_interacao']
                tipo_interacao = dados['tipo_interacao']
                try:
                    watch_duration_seconds = int(dados['watch_duration_seconds']) if dados['watch_duration_seconds'] else 0
                except ValueError:
                    watch_duration_seconds = 0
                    print(f"Erro ao converter watch_duration_seconds para inteiro na linha: {linha}")
                comment_text = dados['comment_text']
                nome_plataforma = dados['nome_plataforma']
                nome_conteudo = dados['nome_conteudo']
                plataforma = self.cadastrar_plataforma(nome_plataforma)
                conteudo = self.__conteudos_registrados.get(nome_conteudo)
                if not conteudo:
                    conteudo = Conteudo(id_conteudo=len(self.__conteudos_registrados) + 1, nome_conteudo=nome_conteudo)
                    self.__conteudos_registrados[nome_conteudo] = conteudo
                usuario = self.__usuarios_registrados.get(usuario_id)
                if not usuario:
                    usuario = Usuario(id_usuario=usuario_id)
                    self.__usuarios_registrados[usuario_id] = usuario
                dados_interacao = {
                    'id_usuario': usuario_id,
                    'timestamp_interacao': timestamp_interacao,
                    'tipo_interacao': tipo_interacao,
                    'watch_duration_seconds': watch_duration_seconds,
                    'comment_text': comment_text
                }
                interacao = Interacao(dados_interacao, conteudo, plataforma)
                conteudo.adicionar_interacao(interacao)
                usuario.registrar_interacao(interacao)
            except ValueError as e:
                print(f"Erro ao processar interação: {e} - Dados: {linha}")
            except KeyError as e:
                print(f"Erro ao processar interação: campo {e} não encontrado - Dados: {linha}")
      
    def gerar_relatorio_engajamento_conteudos(self, top_n=None):
        conteudos = list(self.__conteudos_registrados.values())
        if top_n:
            conteudos = sorted(conteudos, key=lambda c: c.calcular_total_interacoes_engajamento(), reverse=True)[:top_n]
        print()
        print(("-" * 30), "X",("-" * 30))
        print(("-" * 30), "X",("-" * 30))
        print(f"Relatório de Engajamento de Conteúdos (Versão: {self.VERSAO_ANALISE})".center(60))
        print(("-" * 30), "X",("-" * 30))
        print(("-" * 30), "X",("-" * 30))
        print()
        print(f"Total de conteúdos analisados: {len(conteudos)}")
        print(f"Total de usuários registrados: {len(self.__usuarios_registrados)}")
        print(f"Total de plataformas registradas: {len(self.__plataformas_registradas)}")
        print()
        print(("-" * 30), " X ",("-" * 30))
        print()
        for conteudo in conteudos:
            print(f"Conteúdo: {conteudo.nome_conteudo.strip().title()} (ID: {conteudo.id_conteudo})")
            print()
            print(f"  Total de interações de engajamento: {conteudo.calcular_total_interacoes_engajamento()}")
            for tipo, total in conteudo.calcular_contagem_por_tipo_interacao().items():
                print(f"    {tipo}: {total}")
            # print(f"  Contagem por tipo de interação: {conteudo.calcular_contagem_por_tipo_interacao()}")
            print()
            print(f"  Tempo total de consumo: {conteudo.calcular_tempo_total_consumo()} segundos")
            print()
            print(f"  Média de tempo de consumo: {conteudo.calcular_media_tempo_consumo():.2f} segundos")
            print()
            if len(conteudo.listar_comentarios()) > 0:
                print("  Comentários:")
            for i, comment in enumerate(conteudo.listar_comentarios(), start=1):
                print(f"    Comentário {i}: {comment}")
            # for i, comment in conteudo.listar_comentarios():
            #     print(f"    Comentário{i}: {comment}")
            # print(f"  Comentários: {conteudo.listar_comentarios()}\n")
            print()
            print(("-" * 30), " X ",("-" * 30))
            print()
        print()
        print(("-" * 30), "X",("-" * 30))
        print(("-" * 30), "X",("-" * 30))
        print()
        print("Relatório de Engajamento de Conteúdos Finalizado".center(60))
        print()
        print(("-" * 30), "X",("-" * 30))
        print(("-" * 30), "X",("-" * 30))
        print()
        
        return conteudos
    
    def gerar_relatorio_atividade_usuarios(self, top_n=None):
        usuarios = list(self.__usuarios_registrados.values())
        if top_n:
            usuarios = sorted(usuarios, key=lambda u: len(u._Usuario__interacoes_realizadas), reverse=True)[:top_n]
        for usuario in usuarios:
            print(f"\nUsuário ID: {usuario.id_usuario}")
            print(f"  Total de interações: {len(usuario._Usuario__interacoes_realizadas)}")
            print(f"  Conteúdos únicos consumidos: {len(usuario.obter_conteudos_unicos_consumidos())}")
            print("Plataformas mais frequentes:")
            plataformas_frequentes = usuario.plataformas_mais_frequentes()
            for nome_plataforma in plataformas_frequentes:
                plataforma = self.cadastrar_plataforma(nome_plataforma)
                tempo_consumo = usuario.calcular_tempo_total_consumo_plataforma(plataforma)
                print(f" - {plataforma.nome_plataforma}: {tempo_consumo} segundos")

            # plataformas_frequentes = usuario.plataformas_mais_frequentes()
            # for plataforma in plataformas_frequentes:
            #     tempo_consumo = usuario.calcular_tempo_total_consumo_plataforma(plataforma)
            #     print(f"    - {plataforma.nome_plataforma}: {tempo_consumo} segundos")
                # print(f"    - {plataforma} - {tempo_consumo} segundos")
            # print(f"  Tempo total de consumo por plataforma:")
            # for plataforma in self.listar_plataformas():
            #     tempo_consumo = usuario.calcular_tempo_total_consumo_plataforma(plataforma)
            #     print(f"    {plataforma.nome_plataforma}: {tempo_consumo} segundos")
            
            print()
                

            # print(f"  Plataformas mais frequentes: {usuario.plataformas_mais_frequentes()}\n")

        return usuarios
    
    def identificar_top_conteudos(self, metrica, n=5):
        if metrica not in ['tempo_total_consumo', 'total_interacoes_engajamento']:
            raise ValueError("Métrica inválida. Use 'tempo_total_consumo' ou 'total_interacoes_engajamento'.")
        conteudos = list(self.__conteudos_registrados.values())
        if metrica == 'tempo_total_consumo':
            conteudos = sorted(conteudos, key=lambda c: c.calcular_tempo_total_consumo(), reverse=True)[:n]
        elif metrica == 'total_interacoes_engajamento':
            conteudos = sorted(conteudos, key=lambda c: c.calcular_total_interacoes_engajamento(), reverse=True)[:n]
        # print(f"Total de conteúdos analisados: {len(conteudos)}")
        
        print(f"\nTop {n} conteúdos por '{metrica}':")
        print()
        for conteudo in conteudos:
            print(f"Conteúdo: {conteudo.nome_conteudo} (ID: {conteudo.id_conteudo})")
            if metrica == 'tempo_total_consumo':
                print(f"  Tempo total de consumo: {conteudo.calcular_tempo_total_consumo()} segundos")
            elif metrica == 'total_interacoes_engajamento':
                print(f"  Total de interações de engajamento: {conteudo.calcular_total_interacoes_engajamento()}")
            print()
        
        print()
        print(("-" * 20), " X ",("-" * 20))
        print()
        
        print(f"Total de usuários registrados: {len(self.__usuarios_registrados)}")
        print(f"Total de plataformas registradas: {len(self.__plataformas_registradas)}")
        print(f"Versão do sistema de análise: {self.VERSAO_ANALISE}")
        print()

    
    def menu_principal(self):

        while True:
            print("\n" + ("-" * 30))
            print("Bem-vindo ao Sistema de Análise de Engajamento!")
            print(f"Versão: {self.VERSAO_ANALISE}")
            print("Selecione uma opção:")
            print("1. Cadastrar Plataforma")
            print("2. Listar Plataformas")
            print("3. Gerar Relatório de Engajamento de Conteúdos")
            print("4. Gerar Relatório de Atividade de Usuários")
            print("5. Identificar Top Conteúdos")
            print("0. Sair")
            opcao = input("Digite a opção desejada: ")
            print(("-" * 30))
            print()
            if opcao == '1':
                nome_plataforma = input("Digite o nome da plataforma: ")
                plataforma = self.cadastrar_plataforma(nome_plataforma)
                print(f"Plataforma '{plataforma.nome_plataforma}' cadastrada com sucesso!")
            elif opcao == '2':
                plataformas = self.listar_plataformas()
                if plataformas:
                    print("Plataformas registradas:")
                    for plataforma in plataformas:
                        print(f"- {plataforma.nome_plataforma} (ID: {plataforma.id_plataforma})")
                else:
                    print("Nenhuma plataforma registrada.")
            
            elif opcao == '3':
                top_n = input("Deseja ver os top N conteúdos? (Digite um número ou deixe em branco para ver todos): ")
                top_n = int(top_n) if top_n.isdigit() else None
                self.gerar_relatorio_engajamento_conteudos(top_n)
            elif opcao == '4':
                top_n = input("Deseja ver os top N usuários? (Digite um número ou deixe em branco para ver todos): ")
                top_n = int(top_n) if top_n.isdigit() else None
                self.gerar_relatorio_atividade_usuarios(top_n)
            elif opcao == '5':
                metrica = input("Digite a métrica (tempo_total_consumo ou total_interacoes_engajamento): ")
                n = input("Quantos conteúdos deseja ver? (Digite um número): ")
                n = int(n) if n.isdigit() else 5
                self.identificar_top_conteudos(metrica, n)
            elif opcao == '0':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")

    
    # def __str__(self):
    #     return f"Sistema de Análise de Engajamento (Versão: {self.VERSAO_ANALISE})"
    # def __repr__(self):
    #     return f"SistemaAnaliseEngajamento()"