Feature: Login
    Puedo iniciar sesion

    Scenario: Inicio sesion
        Given Tengo mis credenciales de usuario
        And Me sé mis datos para inciar sesión

        When Ingreso mis datos
        And Se envía la solicitud
        
        Then Se crea una cookie de sesion
        And Puedo acceder a mis bug reports