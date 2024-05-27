from urgencia import ColaPrioridad
from urgencia import Paciente
from urgencia import Nodo

def menu():
    urgencias = ColaPrioridad()
    while True:
        print("\n Elija una de las siguientes opciones por favor")
        print("1. Registrar paciente")
        print("2. Consultar próximo paciente")
        print("3. Atender siguiente paciente")
        print("4. Consultar pacientes en espera")
        print("5. Consultar pacientes por triaje")
        print("6. Eliminar paciente")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id = input("Ingrese ID del paciente: ")
            print("Seleccione el género del paciente:")
            print("1. Femenino")
            print("2. Masculino")
            print("3. Otro")
            genero_opcion = input("Ingrese el número correspondiente al género: ")
            if genero_opcion == "1":
                genero = "Femenino"
            elif genero_opcion == "2":
                genero = "Masculino"
            elif genero_opcion == "3":
                genero = "Otro"
            else:
                print("Opción no válida. Intente de nuevo.")
                continue  # Regresa al inicio del bucle para pedir la opción de nuevo

            nombre = input("Ingrese nombre del paciente: ")
            edad = int(input("Ingrese edad del paciente: "))
            triaje = int(input("Ingrese triaje del paciente (1-5): "))
            paciente = Paciente(id, genero, nombre, edad, triaje)
            urgencias.registrar_paciente(paciente)
            print("Paciente registrado exitosamente.")

        elif opcion == "2":
            proximo = urgencias.consultar_proximo()
            if proximo:
                print("Próximo paciente en atención:")
                print(proximo)
            else:
                print("No hay pacientes en espera.")

        elif opcion == "3":
            siguiente = urgencias.atender_siguiente()
            if siguiente:
                print("Paciente atendido:")
                print(siguiente)
            else:
                print("No hay pacientes en espera.")

        elif opcion == "4":
            pacientes = urgencias.consultar_pacientes_espera()
            if pacientes:
                print("Pacientes en espera:")
                for paciente in pacientes:
                    print(paciente)
            else:
                print("No hay pacientes en espera.")

        elif opcion == "5":
            triaje = int(input("Ingrese el triaje a consultar (1-5): "))
            pacientes = urgencias.consultar_pacientes_por_triaje(triaje)
            if pacientes:
                print(f"Pacientes con triaje {triaje}:")
                for paciente in pacientes:
                    print(paciente)
            else:
                print(f"No hay pacientes con triaje {triaje}.")

        elif opcion == "6":
            id_paciente = input("Ingrese el ID del paciente a eliminar: ")
            paciente_eliminado = urgencias.eliminar_paciente(id_paciente)
            if paciente_eliminado:
                print("Paciente eliminado:")
                print(paciente_eliminado)
            else:
                print("No se encontró un paciente con ese ID.")

        elif opcion == "7":
            print("Saliendo del sistema.")


menu()