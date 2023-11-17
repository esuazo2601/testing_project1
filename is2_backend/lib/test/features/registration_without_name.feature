Feature: Registro de Usuario
    Los usuarios pueden registrarse en la plataforma

    Scenario: Intento de registro sin nombre
        Given Quiero registrarme como nuevo usuario
        And No ingreso mi nombre
        When Intento registrarme
        Then Recibo un mensaje de error indicando que todo los parámetros son obligatorios