import grpc
import calculadora_pb2
import calculadora_pb2_grpc

def main():
    with grpc.insecure_channel('localhost:50051') as channel:  # trocar pelo IP do servidor se necessário
        stub = calculadora_pb2_grpc.CalculadoraStub(channel)

        print("=== Calculadora RPC ===")

        while True:
            try:
                a = float(input("Digite o primeiro número: "))
                b = float(input("Digite o segundo número: "))
            except ValueError:
                print("Entrada inválida! Digite um número válido.")
                continue

            op = input("Escolha a operação (+, -, *, /): ")

            if op == '+':
                resposta = stub.Somar(calculadora_pb2.Numeros(a=a, b=b))
            elif op == '-':
                resposta = stub.Subtrair(calculadora_pb2.Numeros(a=a, b=b))
            elif op == '*':
                resposta = stub.Multiplicar(calculadora_pb2.Numeros(a=a, b=b))
            elif op == '/':
                resposta = stub.Dividir(calculadora_pb2.Numeros(a=a, b=b))
            else:
                print("Operação inválida!")
                continue

            print("Resultado:", resposta.valor)

            continuar = input("Deseja fazer outra operação? (s/n): ").lower()
            if continuar != 's':
                print("Saindo da calculadora...")
                break

if __name__ == '__main__':
    main()
