

class Paciente:
    def __init__(self, id, genero, nombre, edad, triaje):
        self.id = id
        self.genero = genero
        self.nombre = nombre 
        self.edad = edad
        self.triaje = triaje

    def __str__(self):
        return f"Id: {self.id}, genero: {self.genero}, nombre: {self.nombre}, edad: {self.edad}, triaje: {self.triaje}"

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijo_izquierdo = None
        self.hijo_derecho = None
        self.padre = None

    def __str__(self, level=0):
        ret = "  " * level + str(self.valor) + "\n"
        if self.hijo_izquierdo:
            ret += self.hijo_izquierdo.__str__(level + 1)
        if self.hijo_derecho:
            ret += self.hijo_derecho.__str__(level + 1)
        return ret
    
class ColaPrioridad:
    def __init__(self):
        self.raiz = None
        self.pacientes = []

    def encolar_paciente(self, paciente):
        self.pacientes.append(paciente)
        self.organizar_arbol()

    def organizar_arbol(self):
        self.raiz = None
        for paciente in self.pacientes:
            self.registrar_paciente(paciente)

    def registrar_paciente(self, paciente):
        nuevo_nodo = Nodo(paciente)
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            nodo_actual = self.raiz
            while True:
                if paciente.triaje < nodo_actual.valor.triaje:
                    if nodo_actual.hijo_izquierdo is None:
                        nodo_actual.hijo_izquierdo = nuevo_nodo
                        nuevo_nodo.padre = nodo_actual
                        break
                    else:
                        nodo_actual = nodo_actual.hijo_izquierdo
                else:
                    if nodo_actual.hijo_derecho is None:
                        nodo_actual.hijo_derecho = nuevo_nodo
                        nuevo_nodo.padre = nodo_actual
                        break
                    else:
                        nodo_actual = nodo_actual.hijo_derecho
            self.comparar_pabre(nuevo_nodo)

    def comparar_pabre(self, nodo):
        while nodo.padre and nodo.valor.triaje < nodo.padre.valor.triaje:
            nodo.valor, nodo.padre.valor = nodo.padre.valor, nodo.valor
            nodo = nodo.padre

    def consultar_proximo(self):
        if self.raiz is None:
            return None
        return self.raiz.valor

    def atender_siguiente(self):
        if self.raiz is None:
            return None
        paciente_atendido = self.raiz.valor
        if self.raiz.hijo_izquierdo is None and self.raiz.hijo_derecho is None:
            self.raiz = None
        else:
            ultimo_nodo = self.obtener_ultimo_nodo(self.raiz)
            self.raiz.valor = ultimo_nodo.valor
            self.eliminar_ultimo_nodo(self.raiz)
            self.reorganizar_cola(self.raiz)
        return paciente_atendido

    def obtener_ultimo_nodo(self, nodo):
        if nodo.hijo_derecho:
            return self.obtener_ultimo_nodo(nodo.hijo_derecho)
        if nodo.hijo_izquierdo:
            return self.obtener_ultimo_nodo(nodo.hijo_izquierdo)
        return nodo

    def eliminar_ultimo_nodo(self, nodo):
        if nodo.hijo_derecho:
            if nodo.hijo_derecho.hijo_derecho is None and nodo.hijo_derecho.hijo_izquierdo is None:
                nodo.hijo_derecho = None
            else:
                self.eliminar_ultimo_nodo(nodo.hijo_derecho)
        elif nodo.hijo_izquierdo:
            if nodo.hijo_izquierdo.hijo_derecho is None and nodo.hijo_izquierdo.hijo_izquierdo is None:
                nodo.hijo_izquierdo = None
            else:
                self.eliminar_ultimo_nodo(nodo.hijo_izquierdo)

    def reorganizar_cola(self, nodo):
        while True:
            menor = nodo
            if nodo.hijo_izquierdo and nodo.hijo_izquierdo.valor.triaje < menor.valor.triaje:
                menor = nodo.hijo_izquierdo
            if nodo.hijo_derecho and nodo.hijo_derecho.valor.triaje < menor.valor.triaje:
                menor = nodo.hijo_derecho
            if menor == nodo:
                break
            nodo.valor, menor.valor = menor.valor, nodo.valor
            nodo = menor

    def eliminar_paciente(self, id_paciente):
        nodo = self.buscar_nodo(self.raiz, id_paciente)
        if nodo is None:
            return None
        if nodo.hijo_izquierdo is None and nodo.hijo_derecho is None:
            if nodo.padre:
                if nodo.padre.hijo_izquierdo == nodo:
                    nodo.padre.hijo_izquierdo = None
                else:
                    nodo.padre.hijo_derecho = None
            else:
                self.raiz = None
        elif nodo.hijo_izquierdo is None:
            if nodo.padre:
                if nodo.padre.hijo_izquierdo == nodo:
                    nodo.padre.hijo_izquierdo = nodo.hijo_derecho
                else:
                    nodo.padre.hijo_derecho = nodo.hijo_derecho
            else:
                self.raiz = nodo.hijo_derecho
            nodo.hijo_derecho.padre = nodo.padre
        elif nodo.hijo_derecho is None:
            if nodo.padre:
                if nodo.padre.hijo_izquierdo == nodo:
                    nodo.padre.hijo_izquierdo = nodo.hijo_izquierdo
                else:
                    nodo.padre.hijo_derecho = nodo.hijo_izquierdo
            else:
                self.raiz = nodo.hijo_izquierdo
            nodo.hijo_izquierdo.padre = nodo.padre
        else:
            sucesor = self.obtener_ultimo_nodo(nodo.hijo_izquierdo)
            nodo.valor = sucesor.valor
            self.eliminar_nodo_sucesor(sucesor)
        self.pacientes = [paciente for paciente in self.pacientes if paciente.id != id_paciente]
        return nodo.valor

    def eliminar_nodo_sucesor(self, nodo):
        if nodo.padre:
            if nodo.padre.hijo_izquierdo == nodo:
                nodo.padre.hijo_izquierdo = None
            else:
                nodo.padre.hijo_derecho = None
        else:
            self.raiz = None

    def buscar_nodo(self, nodo, id_paciente):
        if nodo is None:
            return None
        if nodo.valor.id == id_paciente:
            return nodo
        encontrado = self.buscar_nodo(nodo.hijo_izquierdo, id_paciente)
        if encontrado:
            return encontrado
        return self.buscar_nodo(nodo.hijo_derecho, id_paciente)

    def consultar_pacientes_espera(self):
        return self.listar_pacientes(self.raiz)

    def listar_pacientes(self, nodo):
        pacientes = []
        self.listar_pacientes_rec(nodo, pacientes)
        return pacientes

    def listar_pacientes_rec(self, nodo, pacientes):
        if nodo is not None:
            self.listar_pacientes_rec(nodo.hijo_izquierdo, pacientes)
            pacientes.append(nodo.valor)
            self.listar_pacientes_rec(nodo.hijo_derecho, pacientes)

    def consultar_pacientes_por_triaje(self, triaje):
        return [paciente for paciente in self.consultar_pacientes_espera() if paciente.triaje == triaje]


