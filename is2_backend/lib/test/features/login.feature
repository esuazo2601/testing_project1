Feature: Login
    Puedo iniciar sesion

    Scenario: Inicio sesion
        Given Soy un usuario registrado
        And Me sé mis datos para inciar sesión

        When Ingreso mis datos
        And Se envía la solicitud
        
        Then Se crea una cookie de sesion
        And Puedo acceder a mis bug reports