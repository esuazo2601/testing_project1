Feature: Actualización de Perfil de Usuario

    Scenario: Un usuario actualiza su perfil
        Given Soy el usuario 'Laura' y he iniciado sesión
        When Actualizo mi perfil con un nuevo nombre 'Laura Cid' y cambio mi dirección de correo a 'lauracid@example.com'
        Then Mi perfil se actualiza correctamente con el nuevo nombre y correo