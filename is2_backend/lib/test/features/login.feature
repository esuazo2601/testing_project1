Feature: login
    Puedo iniciar sesion

    Scenario: Inicio sesion
        Given Puedo crear una cuenta
        And Me sé mis datos para inciar sesión

        When Ingreso mis datos
        
        Then Se crea una cookie de sesion