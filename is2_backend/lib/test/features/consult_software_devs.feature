Feature: Consultar softwares asignados a desarrolladores
  Scenario: Un administrador consulta en qué softwares están trabajando los desarrolladores

    Given existen tres desarrolladores: Desarrollador 1, Desarrollador 2, Desarrollador 3
    And existen cuatro softwares: Software A, Software B, Software C, Software D
    And cada desarrollador está asignado a dos softwares, y uno de ellos está asignado a tres
    When el administrador solicita la lista de asignaciones de software a desarrolladores
    Then se muestra correctamente en qué softwares está trabajando cada desarrollador