"""Base de conhecimento para o sistema acadêmico."""

ACADEMIC_DOCUMENTS = [
    {
        "id": "reg_matricula_rematricula",
        "title": "Regulamento de Matricula e Rematricula",
        "content": """
        A Universidade Nova Aurora estabelece as seguintes normas de matricula:

        1. A matricula inicial deve ser realizada dentro do calendario academico oficial.
        2. A rematricula semestral exige quitacao de pendencias academicas e administrativas.
        3. Trancamento de curso pode ser solicitado por ate dois semestres, consecutivos ou nao.
        4. Cancelamento de disciplina e permitido ate a 4a semana letiva.
        5. Alunos com documentacao incompleta ficam com matricula provisoria por ate 30 dias.

        Documentos obrigatorios: identidade, CPF, historico escolar e comprovante de residencia.
        """,
        "category": "regulamentos"
    },
    {
        "id": "reg_avaliacao_aprovacao",
        "title": "Regulamento de Avaliacao e Aprovacao",
        "content": """
        O processo avaliativo segue criterios padronizados por disciplina:

        1. Cada disciplina deve ter no minimo duas avaliacoes formais por semestre.
        2. A nota final varia de 0 a 10.
        3. Aprovacao direta ocorre com nota final igual ou superior a 7,0.
        4. Estudantes com nota entre 4,0 e 6,9 realizam prova de recuperacao.
        5. Apos recuperacao, a media final minima para aprovacao e 5,0.

        Professores devem divulgar criterios e pesos das avaliacoes ate a 2a semana de aula.
        """,
        "category": "regulamentos"
    },
    {
        "id": "reg_frequencia_presenca",
        "title": "Regulamento de Frequencia e Presenca",
        "content": """
        A frequencia minima obrigatoria e de 75% da carga horaria de cada disciplina.

        1. Faltas sao registradas por aula no sistema academico institucional.
        2. Atestados medicos justificam faltas, mas nao abonam automaticamente conteudo e atividades.
        3. Reposicao de atividades depende de autorizacao do docente e da coordenacao.
        4. Alunos abaixo de 75% de presenca sao reprovados por falta, independentemente da nota.
        5. Casos excepcionais sao analisados pelo colegiado de curso.

        O acompanhamento de frequencia e responsabilidade conjunta de aluno e professor.
        """,
        "category": "regulamentos"
    },
    {
        "id": "reg_integridade_academica",
        "title": "Regulamento de Integridade Academica",
        "content": """
        A Universidade adota politica de tolerancia zero para fraude academica.

        1. Sao consideradas infracoes: plagio, cola em prova, falsificacao de documentos e uso indevido de IA sem citacao.
        2. Trabalhos devem apresentar referencias conforme norma institucional.
        3. Em caso de suspeita, o aluno tem direito a defesa formal.
        4. Penalidades incluem advertencia, nota zero, reprovacao na disciplina e suspensao.
        5. Reincidencia pode resultar em desligamento, conforme decisao disciplinar.

        Programas de orientacao sobre etica academica serao oferecidos semestralmente.
        """,
        "category": "regulamentos"
    },
    {
        "id": "reg_biblioteca_recursos",
        "title": "Regulamento de Biblioteca e Recursos de Aprendizagem",
        "content": """
        O uso da biblioteca e dos recursos institucionais segue as normas abaixo:

        1. Cada aluno pode emprestar ate 5 livros por periodo de 14 dias.
        2. Renovacao e permitida uma vez, desde que nao haja reserva ativa.
        3. Atrasos geram bloqueio temporario de novos emprestimos.
        4. Danos ou perda de material exigem reposicao da obra ou pagamento equivalente.
        5. Salas de estudo em grupo devem ser reservadas com antecedencia minima de 24 horas.

        Recursos digitais (bases de dados e periodicos) sao de uso academico exclusivo.
        """,
        "category": "regulamentos"
    }
]

def get_all_documents():
    """Retorna todos os documentos da base de conhecimento."""
    return ACADEMIC_DOCUMENTS
