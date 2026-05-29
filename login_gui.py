import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
import os

# Configuración del tema visual
ctk.set_appearance_mode("System")  # Detecta si la PC usa modo claro u oscuro
ctk.set_default_color_theme("blue")

class VentanaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Sistema de Gestión - U.E. Juana Ramírez")
        self.geometry("500x600")
        
        # ¡Habilitado! Ahora se puede maximizar y estirar la pantalla libremente
        self.resizable(True, True) 

        # --- CONTENEDOR PRINCIPAL (Se mantiene centrado al maximizar) ---
        self.frame = ctk.CTkFrame(master=self, corner_radius=15, width=380, height=500)
        self.frame.pack_propagate(False) # Evita que el cuadro se encoja
        self.frame.pack(expand=True)     # "expand=True" lo mantiene centrado al maximizar

        # --- LOGO / TEXTO INSTITUCIONAL ---
        self.label_titulo = ctk.CTkLabel(
            master=self.frame, 
            text="¡Bienvenido!", 
            font=("Helvetica", 28, "bold")
        )
        self.label_titulo.pack(pady=(40, 5), padx=10)

        self.label_subtitulo = ctk.CTkLabel(
            master=self.frame, 
            text="Control de Matrícula Escolar", 
            font=("Helvetica", 14),
            text_color="gray"
        )
        self.label_subtitulo.pack(pady=(0, 35), padx=10)

        # --- CAMPOS DE ENTRADA (INPUTS) ---
        # Campo de Cédula
        self.input_cedula = ctk.CTkEntry(
            master=self.frame, 
            placeholder_text="Número de Cédula",
            width=280,
            height=45,
            corner_radius=8
        )
        self.input_cedula.pack(pady=12, padx=10)

        # Campo de Contraseña
        self.input_clave = ctk.CTkEntry(
            master=self.frame, 
            placeholder_text="Contraseña", 
            show="*",
            width=280,
            height=45,
            corner_radius=8
        )
        self.input_clave.pack(pady=12, padx=10)

        # --- BOTÓN DE INGRESO ---
        self.boton_ingresar = ctk.CTkButton(
            master=self.frame, 
            text="Iniciar Sesión", 
            command=self.validar_ingreso,
            width=280,
            height=45,
            font=("Helvetica", 15, "bold"),
            corner_radius=8
        )
        self.boton_ingresar.pack(pady=(30, 20), padx=10)

        # Pie de página
        self.label_footer = ctk.CTkLabel(
            master=self.frame, 
            text="Mérida, Venezuela", 
            font=("Helvetica", 11),
            text_color="gray"
        )
        self.label_footer.pack(side="bottom", pady=20)

    def validar_ingreso(self):
        cedula = self.input_cedula.get().strip()
        clave = self.input_clave.get().strip()

        if not cedula or not clave:
            messagebox.showwarning("Campos Vacíos", "Por favor, introduce tu cédula y contraseña.")
            return

        # Verificar si existe la base de datos de usuarios
        if not os.path.exists('personal.csv'):
            messagebox.showerror("Error del Sistema", "No se encontró el archivo 'personal.csv'.\nEjecuta primero 'migrar_personal.py'.")
            return

        try:
            # Leer el archivo de personal
            df_personal = pd.read_csv('personal.csv')
            # Asegurar que la columna 'id' se lea como texto para comparar la cédula perfectamente
            df_personal['id'] = df_personal['id'].astype(str)

            # Buscar al usuario por cédula
            usuario = df_personal[df_personal['id'] == cedula]

            if not usuario.empty:
                # Verificar la contraseña (columna 'contrasena')
                clave_correcta = str(usuario.iloc[0]['contrasena']).strip()
                nombre_usuario = usuario.iloc[0]['nombre']
                rol_usuario = usuario.iloc[0]['rol']

                if clave == clave_correcta:
                    messagebox.showinfo("Acceso Concedido", f"Bienvenido(a): {nombre_usuario}\nRol: {rol_usuario}")
                    
                    # Aquí cerraremos esta ventana y abriremos el menú principal gráfico
                    # self.destroy() 
                else:
                    messagebox.showerror("Error de Acceso", "La contraseña es incorrecta.")
            else:
                messagebox.showerror("Error de Acceso", "La cédula ingresada no está registrada como personal autorizado.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer la base de datos: {e}")

if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()