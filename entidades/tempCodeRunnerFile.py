    if not isinstance(interacao, Interacao):
            raise ValueError(f"Interação deve ser uma instância da classe Interacao, mas foi passado um objeto do tipo {type(interacao).__name__}")
        if interacao not in self.__interacoes_realizadas:
            self.__interacoes_realizadas.append(interacao)