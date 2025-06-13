from analise.sistema import SistemaAnaliseEngajamento
from entidades.usuario import Usuario
from entidades.conteudo import Podcast, Video, Artigo, Conteudo
from entidades.interacao import Interacao
from entidades.plataforma import Plataforma


def main():
    # Inicializar o sistema de análise de engajamento
    # Processar interações do CSV
    sistema = SistemaAnaliseEngajamento()
    sistema.processar_interacoes_do_csv('interacoes_globo.csv')
    sistema.menu_principal()
    # Gerar relatórios de engajamento e atividade dos usuários
    # sistema.gerar_relatorio_engajamento_conteudos()
    # sistema.gerar_relatorio_atividade_usuarios()
    # Identificar os top conteúdos com base no tempo total de consumo e total de interações de engajamento
    # sistema.identificar_top_conteudos('tempo_total_consumo', n=5)
    # sistema.identificar_top_conteudos('total_interacoes_engajamento', n=5)

    # # Exemplo de uso do usuário e interações
    # # Criar um usuário e registrar interações

    # usuario = Usuario(id_usuario=1)
    # # Exemplo de uso do usuário
    # # Criar interações com diferentes tipos de conteúdo
    # # e registrar essas interações
    # podcast = Podcast(id_conteudo=1, nome_conteudo='Podcast de Teste', duracao_total_episodio_seg=3600)
    # interacao = Interacao(
    #     dados_brutos={
    #         'id_usuario': usuario.id_usuario,
    #         'timestamp_interacao': '2023-10-01T12:00:00',
    #         'tipo_interacao': 'like',
    #         'watch_duration_seconds': 300,
    #         'comment_text': ''
    #     },
    #     conteudo_associado=podcast,
    #     plataforma_interacao= Plataforma('spotfy')
    # )
    # usuario.registrar_interacao(interacao)

    # video = Video(id_conteudo=2, nome_conteudo='Video de Teste', duracao_total_video_seg=1800)
    # interacao2 = Interacao(
    #     dados_brutos={
    #         'id_usuario': usuario.id_usuario,
    #         'timestamp_interacao': '2023-10-01T12:02:00',
    #         'tipo_interacao': 'view_start',
    #         'watch_duration_seconds': 1200,
    #         'comment_text': ''
    #     },
    #     conteudo_associado=video,
    #     plataforma_interacao=Plataforma('youtube')
    # )
    # usuario.registrar_interacao(interacao2)

    # artigo = Artigo(id_conteudo=3, nome_conteudo='Artigo de Teste', tempo_leitura_estimado_seg=600)
    # interacao3 = Interacao(
    #     dados_brutos={
    #         'id_usuario': usuario.id_usuario,
    #         'timestamp_interacao': '2023-10-01T12:05:00',
    #         'tipo_interacao': 'comment',
    #         'watch_duration_seconds': 0,
    #         'comment_text': 'Ótimo artigo!'
    #     },
    #     conteudo_associado=artigo,
    #     plataforma_interacao=Plataforma('medium')
    # )

    # artigo.adicionar_interacao(interacao3)

    # usuario.registrar_interacao(interacao3)

    # video2 = Video(id_conteudo=4, nome_conteudo='Outro Video de Teste', duracao_total_video_seg=2400)
    # interacao4 = Interacao(
    #     dados_brutos={
    #         'id_usuario': usuario.id_usuario,
    #         'timestamp_interacao': '2023-10-01T12:10:00',
    #         'tipo_interacao': 'comment',
    #         'watch_duration_seconds': 0,
    #         'comment_text': 'Massa o vídeo!'
    #     },
    #     conteudo_associado=video2,
    #     plataforma_interacao=Plataforma('youtube')
    # )
    # video2.adicionar_interacao(interacao4)
    # usuario.registrar_interacao(interacao4)

    # conteudo = Conteudo(id_conteudo=5, nome_conteudo='Conteúdo Genérico')
    # interacao5 = Interacao(
    #     dados_brutos={
    #         'id_usuario': usuario.id_usuario,
    #         'timestamp_interacao': '2023-10-01T12:15:00',
    #         'tipo_interacao': 'share',
    #         'watch_duration_seconds': 0,
    #         'comment_text': ''
    #     },
    #     conteudo_associado=conteudo,
    #     plataforma_interacao=Plataforma('twitter')
    # )

    # conteudo.adicionar_interacao(interacao5)
    # usuario.registrar_interacao(interacao5)
    

    # usuario.obter_interacoes_por_tipo('like')
    # usuario.obter_interacoes_por_tipo('view_start')
    # usuario.obter_interacoes_por_tipo('comment')
    

    
    
    
    
   
    
if __name__ == '__main__':
    main()