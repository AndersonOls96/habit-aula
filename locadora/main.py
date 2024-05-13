from classes import *

localiza = Locadora()

localiza.adicionar_veiculo(Carro('VW', 'Gol', '2023', 4))
localiza.adicionar_veiculo(Carro('Fiat', 'Argo', '2024', 4))
localiza.adicionar_veiculo(Carro('Reanault', 'Kwid', '2022', 4))

localiza.adicionar_veiculo(Motocicleta('Honda', 'CG', '2022', 125))
localiza.adicionar_veiculo(Motocicleta('Yamaha', 'XRE', '2022', 300))

print("Veículos disponíveis na locadora: ")
localiza.mostrar_veiculos()


localiza.alugar_veiculo("Argo")

print('Veiculos disponiveis após o aluguel')
localiza.mostrar_veiculos()
