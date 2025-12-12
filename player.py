# player.py 

class Jogador:
   
    def __init__(self, nome, data_nascimento, senha, nivel=1, fase=1, xp=0, nivel_conhecimento="Iniciante"):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.senha = senha
        self.nivel = nivel
        self.fase = fase
        self.xp = xp
        self.nivel_conhecimento = nivel_conhecimento

    @classmethod
    def from_dict(cls, nome, dados: dict):
       
        return cls(
            nome,
            dados.get("data_nascimento"),
            dados.get("senha"),
            dados.get("nivel", 1),
            dados.get("fase", 1),
            dados.get("xp", 0),
            dados.get("nivel_conhecimento", "Iniciante")
        )

    def to_dict(self):
        return {
            "data_nascimento": self.data_nascimento,
            "senha": self.senha,
            "nivel": self.nivel,
            "fase": self.fase,
            "xp": self.xp,
            "nivel_conhecimento": self.nivel_conhecimento,
        }

    def __repr__(self):
        return f"<Jogador {self.nome} fase={self.fase} nível={self.nivel}>"