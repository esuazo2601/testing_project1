Feature: Asignar desarrollador a software
  Scenario: Un administrador asigna un desarrollador a un software
      Given existe un software llamado "Software de prueba"
      And existe un desarrollador llamado Felipe
      When el administrador asigna a Felipe al "Software de prueba"
      Then se confirma que Felipe ha sido asignado correctamente al "Software de prueba"