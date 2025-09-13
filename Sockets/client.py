import socket

HOST = '127.0.0.1'  # IP do servidor
PORT = 5001

def main():
    #socket do cliente
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connect: cliente tenta se conectar ao servidor
    client.connect((HOST, PORT)) 
    while True:
        print("\n1 - Cadastrar pessoa")
        print("2 - Listar cadastros")
        print("3 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            numero = input("Número de Telefone: ")
            idade = input("Idade: ")
            profissao = input("Profissão: ")
            msg = f"CADASTRAR|{nome}|{numero}|{idade}|{profissao}"
            # Write: envia ao servidor
            client.send(msg.encode())

        elif opcao == "2":
            client.send("LISTAR".encode())

        elif opcao == "3":
            client.send("SAIR".encode())
            break
        else:
            print("Opção inválida!")
            continue
        
        #Read: recebe resposta do servidor
        resposta = client.recv(1024).decode()
        print(f"\n[RESPOSTA DO SERVIDOR]\n{resposta}")

    client.close()

if __name__ == "__main__":
    main()
