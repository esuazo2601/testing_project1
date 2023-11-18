Feature: Reasignación de Reportes
  Los desarrolladores solicitan reasignación de reportes

  Scenario: Un desarrollador solicita la reasignación de un reporte
    Given Un desarrollador con un reporte asignado
    When El desarrollador solicita la reasignación del reporte
    Then La reasignación se crea correctamente