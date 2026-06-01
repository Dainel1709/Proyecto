import pandas as pd

def migrar_pdf_admin_a_personal():
    print("=== MIGRANDO PERSONAL DESDE PDF/TEXTO EXTRAÍDO ===")
    
    datos_personal = [
        {"id": "17238770", "nombre": "Lorena Carolina Rangel Ramirez", "rol": "Directora", "contrasena": "1234"},
        {"id": "17129781", "nombre": "Lin Marbely Uzcategui Briceno", "rol": "Administrativo", "contrasena": "1234"},
        {"id": "15031556", "nombre": "Yenith Del Carmen Davila Briceno", "rol": "Administrativo", "contrasena": "1234"},
        {"id": "22655385", "nombre": "Stivenso Aldana Davila", "rol": "Profesora", "contrasena": "1234"},
        {"id": "20850552", "nombre": "Suleima Elena Sulbaran Parra", "rol": "Profesora", "contrasena": "1234"},
        {"id": "17340678", "nombre": "Ana Teresa Sanchez Rivera", "rol": "Profesora", "contrasena": "1234"},
        {"id": "14700233", "nombre": "Luisa Eulalia Quintero Rangel", "rol": "Profesora", "contrasena": "1234"},
        {"id": "17238934", "nombre": "Maria Fernanda Sanchez Parra", "rol": "Profesora", "contrasena": "1234"},
        {"id": "18309890", "nombre": "Norelkys Del Carmen Albarran Balza", "rol": "Profesora", "contrasena": "1234"},
        {"id": "17130801", "nombre": "Milagros Del Valle Davila Briceno", "rol": "Profesora", "contrasena": "1234"},
        {"id": "27780603", "nombre": "Genesis Del Valle Albarran Villarreal", "rol": "Profesora", "contrasena": "1234"},
        {"id": "24229244", "nombre": "Stefany Yurinay Balza Trejo", "rol": "Profesora", "contrasena": "1234"},
        {"id": "11951936", "nombre": "Flavio Guzman Briceno Segovia", "rol": "Profesora", "contrasena": "1234"},
        {"id": "11953316", "nombre": "Yuraima Del Carmen Pena De Quintero", "rol": "Administrativo", "contrasena": "1234"}
    ]
    
    # Crear el DataFrame y guardarlo
    df_personal = pd.DataFrame(datos_personal)
    df_personal.to_csv('personal.csv', index=False)
    
    print(f"\n[ÉXITO] Se registraron {len(datos_personal)} empleados autorizados para usar el sistema.")
    print("Archivo 'personal.csv' actualizado correctamente.")
    print("\n--- CÓMO INICIAR SESIÓN ---")
    print("1. Directora: Usa la cédula 17238770 (Clave: 1234)")
    print("2. Administrativos: Usa cédulas como 17129781 o 11953316 (Clave: 1234)")
    print("3. Profesores: Usa cédulas como 17340678 o 14700233 (Clave: 1234)")

if __name__ == "__main__":
    migrar_pdf_admin_a_personal()
