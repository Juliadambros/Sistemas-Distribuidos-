import grpc
from concurrent import futures
import calculadora_pb2
import calculadora_pb2_grpc
import threading

cliente_contador = 0
contador_lock = threading.Lock()  # Para garantir segurança em multithreading

class CalculadoraService(calculadora_pb2_grpc.CalculadoraServicer):
    def __init__(self):
        self.clientes = {}  # Dicionário para mapear context.peer() -> número do cliente

    def _get_cliente_numero(self, context):
        global cliente_contador
        peer = context.peer()
        with contador_lock:
            if peer not in self.clientes:
                cliente_contador += 1
                self.clientes[peer] = cliente_contador
        return self.clientes[peer]

    def Somar(self, request, context):
        numero_cliente = self._get_cliente_numero(context)
        print(f"Cliente {numero_cliente} solicitou SOMAR: {request.a} + {request.b}")
        return calculadora_pb2.Resultado(valor=request.a + request.b)

    def Subtrair(self, request, context):
        numero_cliente = self._get_cliente_numero(context)
        print(f"Cliente {numero_cliente} solicitou SUBTRAIR: {request.a} - {request.b}")
        return calculadora_pb2.Resultado(valor=request.a - request.b)

    def Multiplicar(self, request, context):
        numero_cliente = self._get_cliente_numero(context)
        print(f"Cliente {numero_cliente} solicitou MULTIPLICAR: {request.a} * {request.b}")
        return calculadora_pb2.Resultado(valor=request.a * request.b)

    def Dividir(self, request, context):
        numero_cliente = self._get_cliente_numero(context)
        print(f"Cliente {numero_cliente} solicitou DIVIDIR: {request.a} / {request.b}")
        if request.b == 0:
            print("Divisão por zero detectada!")
            return calculadora_pb2.Resultado(valor=0)
        return calculadora_pb2.Resultado(valor=request.a / request.b)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculadora_pb2_grpc.add_CalculadoraServicer_to_server(CalculadoraService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor RPC rodando na porta 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
