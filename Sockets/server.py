import socket
import threading
import json

HOST = '0.0.0.0' # aceitar conexões de qualquer IP, para quando rodar em máquinas diferentes 
PORT = 5001
ARQUIVO = "cadastros.json"

cadastros = []  

def salvar_em_arquivo():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(cadastros, f, ensure_ascii=False, indent=4)

def carregar_do_arquivo():
    global cadastros
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            cadastros = json.load(f)
    except FileNotFoundError:
        cadastros = []

def handle_client(conn, addr):
    print(f"[NOVA CONEXÃO] {addr}")
    while True:
        try:
            #Read (recebendo dados do cliente)
            data = conn.recv(1024).decode()
            if not data:
                break

            parts = data.split("|")

            if parts[0] == "CADASTRAR":
                nome, numero, idade, profissao = parts[1:]
                cadastros.append({
                    "nome": nome,
                    "numero": numero,
                    "idade": idade,
                    "profissao": profissao
                })
                salvar_em_arquivo()  

                print(f"[CADASTRO] {nome} - {idade} anos - {profissao} (tel: {numero})")
                #Write (enviando resposta ao cliente)
                conn.send("Cadastro realizado com sucesso!".encode())

            elif parts[0] == "LISTAR":
                if cadastros:
                    resposta = "\n".join([
                        f"{c['nome']} - {c['idade']} anos - {c['profissao']} (tel: {c['numero']})"
                        for c in cadastros
                    ])
                else:
                    resposta = "Nenhum cadastro encontrado."
                conn.send(resposta.encode())
                print(f"[LISTA SOLICITADA] {addr}")

            elif parts[0] == "SAIR":
                print(f"[DESCONECTADO] {addr}")
                break

        except Exception as e:
            print(f"[ERRO] {e}")
            break

    conn.close()


def main():
    carregar_do_arquivo()  

    #cria o socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Bind: associa o IP e a porta ao servidor
    server.bind((HOST, PORT))
    #Listen: coloca o servidor em modo de espera
    server.listen()
    print(f"[SERVIDOR INICIADO] Aguardando em {HOST}:{PORT}")

    while True:
        #Accept: aceita uma conexão e cria um novo socket para o cliente
        conn, addr = server.accept()
        #thread para lidar com esse cliente sem travar o servidor
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()

