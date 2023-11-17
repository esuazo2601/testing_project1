Feature: Login
  Scenario: Intento de inicio de sesión con contraseña dudosa
    Given Tengo mis credenciales de usuario
    And Soy un usuario registrado
    When Intento iniciar sesión con una contraseña que no recuerdo bien
    Then Se muestra un error de "Contraseña incorrecta"