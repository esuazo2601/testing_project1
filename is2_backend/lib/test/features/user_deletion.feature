Feature: Eliminación de Cuenta de Usuario

    Scenario: Un usuario elimina su cuenta

        Given Soy el usuario 'Carlos' y he iniciado sesión
        When Elijo eliminar mi cuenta
        Then Mi cuenta se elimina correctamente y ya no puedo iniciar sesión