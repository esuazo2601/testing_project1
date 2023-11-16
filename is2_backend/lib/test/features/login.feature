Feature: Login
    Puedo iniciar sesion

    Scenario: Inicio sesion
        Given Tengo mis credenciales de usuario
        And Soy un usuario registrado
        When Ingreso mis datos
        Then Se crea una cookie de sesión
        And Puedo acceder a mis bug reports