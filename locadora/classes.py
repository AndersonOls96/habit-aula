class Veiculo:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.alugado = False

    def mostrar_informacoes(self):
        print(f'Marca: {self.marca}, Modelo: {self.modelo}, Ano: {self.ano}, '
        f'Alugado: {'Sim' if self.alugado else 'Não'}')
    
    def alugar(self):
        if not self.alugado:
            self.alugado = True
            print(f'{self.modelo} alugado com sucesso!')
        else:
            print(f'{self.modelo} já está alugado!')
    
    def devolver(self):
        if self.alugado:
            self.alugado = False
            print(f'{self.modelo} devolvido com sucesso!')
        else:
            print(f'{self.modelo} não está alugado!')

class Carro(Veiculo):
    def __init__(self, marca, modelo, ano, portas):
        super().__init__(marca, modelo, ano)
        self.portas = portas
    
    def mostrar_informacoes(self):
        super().mostrar_informacoes()
        print(f'Portas: {self.portas}')

class Motocicleta(Veiculo):
    def __init__(self, marca, modelo, ano, cilindradas):
        super().__init__(marca, modelo, ano)
        self.cilindradas = cilindradas
    
    def mostrar_informacoes(self):
        super().mostrar_informacoes()
        print(f'Cilindradas: {self.cilindradas}')


class Locadora:
    def __init__(self):
        self.veiculos = []
    
    def adicionar_veiculo(self, veiculo):
        self.veiculos.append(veiculo)

    def mostrar_veiculos(self):
        for veiculo in self.veiculos:
            veiculo.mostrar_informacoes()
    
    def alugar_veiculo(self, modelo):
        for veiculo in self.veiculos:
            if veiculo.modelo == modelo and not veiculo.alugado:
                veiculo.alugar()
                return
        print(f'{modelo} não disponível para aluguel.')
    
    def devolver_veiculo(self, modelo):
        for veiculo in self.veiculos:
            if veiculo.modelo == modelo and veiculo.alugado:
                veiculo.devolver()
                return
        print(f'{modelo} não estava alugado.')
