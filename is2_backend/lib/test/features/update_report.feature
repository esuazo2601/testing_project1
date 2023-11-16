Feature: Actualización de Reportes

    Scenario: Un usuario crea y luego actualiza la información de un reporte
        Given Soy un usuario registrado y he iniciado sesión
        And He creado un nuevo reporte
        When Actualizo el título y la descripción de mi reporte
        Then El reporte se actualiza correctamente con el nuevo título y descripción