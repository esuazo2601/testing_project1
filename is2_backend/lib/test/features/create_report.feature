Feature: Crear un reporte
    Siendo un usuario puedo crear un reporte

Scenario: Creacion de un reporte
    Given Que existe un software
    And Soy un usuario registrado en la base de datos
    And El software existe en la base de datos
    
    When Intento crear un reporte 
    Then Se crea un reporte asociado a ese software
