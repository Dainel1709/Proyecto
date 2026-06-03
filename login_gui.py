import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import os
import migrar_excel

# Configuración del tema visual global
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

# ==========================================
# 1. CONTENEDOR: PANTALLA DE LOGIN
# ==========================================
class FrameLogin(ctk.CTkFrame):
    def __init__(self, master, callback_login_exitoso):
        super().__init__(master, fg_color="transparent")
        self.callback_login_exitoso = callback_login_exitoso

        # Cuadro centrado de Login
        self.card = ctk.CTkFrame(master=self, corner_radius=15, width=380, height=500)
        self.card.pack_propagate(False)
        self.card.pack(expand=True)     

        # Títulos
        self.label_titulo = ctk.CTkLabel(master=self.card, text="¡Bienvenido!", font=("Helvetica", 28, "bold"))
        self.label_titulo.pack(pady=(40, 5), padx=10)

        self.label_subtitulo = ctk.CTkLabel(master=self.card, text="Control de Matrícula Escolar", font=("Helvetica", 14), text_color="gray")
        self.label_subtitulo.pack(pady=(0, 35), padx=10)

        # Campos de texto
        self.input_cedula = ctk.CTkEntry(master=self.card, placeholder_text="Número de Cédula", width=280, height=45, corner_radius=8)
        self.input_cedula.pack(pady=12, padx=10)

        self.input_clave = ctk.CTkEntry(master=self.card, placeholder_text="Contraseña", show="*", width=280, height=45, corner_radius=8)
        self.input_clave.pack(pady=12, padx=10)

        # Botón
        self.boton_ingresar = ctk.CTkButton(master=self.card, text="Iniciar Sesión", command=self.validar_ingreso, width=280, height=45, font=("Helvetica", 15, "bold"), corner_radius=8)
        self.boton_ingresar.pack(pady=(30, 20), padx=10)

        self.label_footer = ctk.CTkLabel(master=self.card, text="Mérida, Venezuela", font=("Helvetica", 11), text_color="gray")
        self.label_footer.pack(side="bottom", pady=20)

        # Navegación entre campos
        self.input_cedula.bind("<Return>", self.pasar_a_contrasena)
        self.input_cedula.bind("<Down>", self.pasar_a_contrasena)
        self.input_clave.bind("<Return>", self.validar_ingreso)
        self.input_clave.bind("<Up>", self.regresar_a_cedula)  
        
        self.input_cedula.focus()

    def pasar_a_contrasena(self, event=None):
        self.input_clave.focus()

    def regresar_a_cedula(self, event=None):  
        self.input_cedula.focus()

    def validar_ingreso(self, event=None): 
        cedula = self.input_cedula.get().strip() 
        clave = self.input_clave.get().strip() 

        if not cedula or not clave: 
            messagebox.showwarning("Campos Vacíos", "Por favor, introduce tu cédula y contraseña.") 
            return 

        if not os.path.exists('personal.csv'): 
            messagebox.showerror("Error del Sistema", "No se encontró el archivo 'personal.csv'.") 
            return 

        try: 
            df_personal = pd.read_csv('personal.csv') 
            df_personal['id'] = df_personal['id'].astype(str) 
            usuario = df_personal[df_personal['id'] == cedula] 

            if not usuario.empty: 
                clave_correcta = str(usuario.iloc[0]['contrasena']).strip() 
                nombre_usuario = usuario.iloc[0]['nombre'] 
                rol_usuario = usuario.iloc[0]['rol'] 

                if clave == clave_correcta: 
                    self.callback_login_exitoso(nombre_usuario, rol_usuario) 
                else: 
                    messagebox.showerror("Error de Acceso", "La contraseña es incorrecta.") 
            else: 
                messagebox.showerror("Error de Acceso", "Cédula no registrada.") 
        except Exception as e: 
            messagebox.showerror("Error", f"No se pudo leer la base de datos: {e}")


# ==========================================
# 2. CONTENEDOR: PANTALLA MENÚ PRINCIPAL
# ==========================================
class FrameMenuPrincipal(ctk.CTkFrame):
    def __init__(self, master, nombre_usuario, rol_usuario, callback_cerrar_sesion):
        super().__init__(master, fg_color="transparent")
        self.nombre = nombre_usuario
        self.rol = rol_usuario
        self.callback_cerrar_sesion = callback_cerrar_sesion
        self.menu_estudiantes_abierto = False
        self.df_actual = None

        # --- CONFIGURACIÓN DE LA BARRA LATERAL ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1) 
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="U.E. Juana Ramírez", font=("Helvetica", 18, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 10))
        self.user_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.user_frame.grid(row=1, column=0, padx=10, pady=(0, 20))   
        self.lbl_user_name = ctk.CTkLabel(self.user_frame, text=self.nombre, font=("Helvetica", 13, "bold"), wraplength=180)
        self.lbl_user_name.pack()
        self.lbl_user_role = ctk.CTkLabel(self.user_frame, text=f"Rol: {self.rol}", font=("Helvetica", 11), text_color="#1f538d")
        self.lbl_user_role.pack()

        # --- BOTONES DE MENÚ LATERAL ---
        self.btn_estudiantes = ctk.CTkButton(self.sidebar_frame, text="Estudiantes ▼", command=self.toggle_menu_estudiantes, height=35)
        self.btn_estudiantes.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.btn_ver_matricula = ctk.CTkButton(self.sidebar_frame, text="   Ver Matrícula Escolar", command=self.vista_ver_matricula, height=35)
        self.btn_notas = ctk.CTkButton(self.sidebar_frame, text="   Cargar Notas / Asistencia", command=self.vista_notas, height=35)
        
        if self.rol in ["Directora", "Administrativo"]:
            self.btn_carga_inicial = ctk.CTkButton(self.sidebar_frame, text="⚙️ Carga Inicial (XLSX->CSV)", fg_color="#1a6332", hover_color="#114221", command=self.ejecutar_carga_inicial, height=35)
            self.btn_carga_inicial.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
            
            self.btn_admin = ctk.CTkButton(self.sidebar_frame, text="   Modificar Alumnos (Admin)", fg_color="#2b719e", command=self.vista_administrar, height=35)

        self.btn_salir = ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión", fg_color="#912a2a", hover_color="#701e1e", command=self.callback_cerrar_sesion, height=35)
        self.btn_salir.grid(row=9, column=0, padx=20, pady=20, sticky="ew")

        # --- CONTENIDO DERECHO ---
        self.contenido_frame = ctk.CTkFrame(self, fg_color="transparent") 
        self.contenido_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.contenido_frame.grid_columnconfigure(0, weight=1)
        self.contenido_frame.grid_rowconfigure(3, weight=1)
        
        self.lbl_bienvenida = ctk.CTkLabel(self.contenido_frame, text=f"¡Hola, {self.nombre.split()[0]}!", font=("Helvetica", 22, "bold"), anchor="w")
        self.lbl_bienvenida.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        self.lbl_info_seccion = ctk.CTkLabel(self.contenido_frame, text="Selecciona una opción para arrancar.", font=("Helvetica", 13), text_color="gray", anchor="w")
        self.lbl_info_seccion.grid(row=1, column=0, padx=10, pady=(0, 15), sticky="w")

        # Panel de Filtro Superior
        self.frame_grados = ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        self.lbl_selector = ctk.CTkLabel(self.frame_grados, text="Grado:", font=("Helvetica", 13, "bold"))
        self.lbl_selector.pack(side="left", padx=5)
        self.combo_grado = ctk.CTkOptionMenu(self.frame_grados, values=["1er Grado", "2do Grado", "3er Grado", "4to Grado", "5to Grado", "6to Grado"], command=self.cargar_estudiantes_por_grado, width=150)
        self.combo_grado.pack(side="left", padx=5)

        # Configuración de Tabla
        columnas = ('Numero de lista','Cédula Escolar','Cédula Identidad', 'Estudiante', 'Genero', 'Fecha de nacimiento')
        self.tabla = ttk.Treeview(self.contenido_frame, columns=columnas, show='headings')
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120)
        self.tabla.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.tabla.bind("<<TreeviewSelect>>", self.controlar_visibilidad_boton)

        # Contenedor inferior dinámico para los botones de acción en horizontal
        self.frame_acciones_db = ctk.CTkFrame(self.contenido_frame, fg_color="transparent")
        
        self.btn_detalle = ctk.CTkButton(self.frame_acciones_db, text="🔎 Ver / Editar Ficha Completa")
        self.btn_eliminar = ctk.CTkButton(self.frame_acciones_db, text="❌ Eliminar Alumno", fg_color="#912a2a", hover_color="#701e1e", command=self.ejecutar_eliminar_alumno)
        self.btn_agregar = ctk.CTkButton(self.frame_acciones_db, text="➕ Añadir Nuevo Alumno", fg_color="#1a6332", hover_color="#114221", command=self.mostrar_ventana_agregar)

        self.pantalla_datos = ctk.CTkTextbox(self.contenido_frame, font=("Courier New", 12), corner_radius=10)

    def toggle_menu_estudiantes(self):
        if not self.menu_estudiantes_abierto:
            self.btn_ver_matricula.grid(row=3, column=0, padx=20, pady=3, sticky="ew")
            self.btn_notas.grid(row=4, column=0, padx=20, pady=3, sticky="ew")
            if hasattr(self, 'btn_admin'): self.btn_admin.grid(row=5, column=0, padx=20, pady=3, sticky="ew")
            self.btn_estudiantes.configure(text="Estudiantes ▲")
            self.menu_estudiantes_abierto = True
        else:
            self.btn_ver_matricula.grid_forget()
            self.btn_notas.grid_forget()
            if hasattr(self, 'btn_admin'): self.btn_admin.grid_forget()
            self.btn_estudiantes.configure(text="Estudiantes ▼")
            self.menu_estudiantes_abierto = False

    def controlar_visibilidad_boton(self, event=None):
        """Gestiona la aparición dinámica de los botones basados en la sección actual."""
        es_modulo_admin = "Sección de control de matrícula" in self.lbl_info_seccion.cget("text")

        if self.tabla.selection():
            self.btn_detalle.grid(row=0, column=0, padx=10)
            if es_modulo_admin:
                self.btn_eliminar.grid(row=0, column=1, padx=10)
            else:
                self.btn_eliminar.grid_forget()
        else:
            self.btn_detalle.grid_forget()
            self.btn_eliminar.grid_forget()

    def vista_ver_matricula(self):
        # Desaparecer el contenedor y forzar limpieza de botones críticos
        self.frame_acciones_db.grid_forget()
        self.btn_eliminar.grid_forget()
        self.btn_agregar.grid_forget()
        
        self.frame_grados.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        self.lbl_info_seccion.configure(text="Visualizando las listas oficiales desglosadas por grados.")
        self.btn_detalle.configure(text="🔎 Ver Representante", command=self.mostrar_solo_lectura_representante, fg_color="#1a6332", hover_color="#114221")
        
        self.pantalla_datos.grid_forget()
        self.tabla.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        self.frame_acciones_db.grid(row=4, column=0, pady=15)
        self.cargar_estudiantes_por_grado(self.combo_grado.get())

    def vista_notas(self):
        self.frame_acciones_db.grid_forget()
        self.btn_eliminar.grid_forget()
        self.btn_agregar.grid_forget()
        self.tabla.grid_forget()
        
        self.frame_grados.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        self.lbl_info_seccion.configure(text="Módulo para el registro de calificaciones y asistencias por lapsos.")
        
        self.pantalla_datos.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.pantalla_datos.configure(state="normal")
        self.pantalla_datos.delete("0.0", "end")
        self.pantalla_datos.insert("0.0", f"=== CARGA DE NOTAS Y EVALUACIÓN ===\n\nDocente: {self.nombre}\nGrado Consultando: {self.combo_grado.get()}\n\nEstatus: Sección en desarrollo institucional...")
        self.pantalla_datos.configure(state="disabled")

    def vista_administrar(self):
        self.frame_acciones_db.grid_forget()
        self.btn_detalle.grid_forget()
        self.btn_eliminar.grid_forget()
        
        self.frame_grados.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        self.lbl_info_seccion.configure(text="Sección de control de matrícula. Los cambios se inyectarán en el CSV y Excel oficial.")
        self.btn_detalle.configure(text="⚙️ Administrar Ficha Alumno", command=self.mostrar_detalle_y_edicion, fg_color="#1f538d", hover_color="#14375e")
        
        self.pantalla_datos.grid_forget()
        self.tabla.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        # Posicionar contenedor e inyectar el botón de Agregar únicamente aquí
        self.frame_acciones_db.grid(row=4, column=0, pady=15)
        self.btn_agregar.grid(row=0, column=2, padx=10)
        
        self.cargar_estudiantes_por_grado(self.combo_grado.get())

    def cargar_estudiantes_por_grado(self, grado_seleccionado):
        self.btn_detalle.grid_forget()
        self.btn_eliminar.grid_forget()
        nombre_archivo = f"{grado_seleccionado.lower().replace(' ', '_')}.csv"
        for item in self.tabla.get_children(): self.tabla.delete(item)
        
        if os.path.exists(nombre_archivo):
            try:
                self.df_actual = pd.read_csv(nombre_archivo, dtype=str)
                for _, row in self.df_actual.iterrows():
                    self.tabla.insert("", "end", values=(
                        row.get('Número de lista', ''), row.get('Cédula Escolar', ''),
                        row.get('Cédula Identidad', ''), row.get('Estudiante', ''), 
                        row.get('Genero', ''), row.get('Fecha de nacimiento', '')
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
        else:
            self.df_actual = None

    def ejecutar_carga_inicial(self):
        confirmar = messagebox.askyesno("Confirmación", "¿Desea escanear los archivos Excel oficiales para crear las listas .CSV por primera vez?")
        if confirmar:
            exito = migrar_excel.migrar_por_grados_separados()
            if exito:
                messagebox.showinfo("Proceso Completo", "Se migraron las listas Excel a formato CSV exitosamente.")
                self.cargar_estudiantes_por_grado(self.combo_grado.get())
            else:
                messagebox.showwarning("Aviso", "No se encontraron nuevos archivos de Matrícula .xlsx o no tenían datos correctos.")

    def ejecutar_eliminar_alumno(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado: return
        
        valores = self.tabla.item(item_seleccionado)['values']
        cedula_esc = str(valores[1])
        cedula_id = str(valores[2])
        nombre_alumno = valores[3]
        grado_actual = self.combo_grado.get()
        
        cedula_llave = cedula_id if cedula_id != "No posee" else cedula_esc
        
        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Está completamente seguro de eliminar permanentemente al alumno {nombre_alumno} de la institución?")
        if confirmar:
            exito, msg = migrar_excel.eliminar_estudiante_en_csv(grado_actual, cedula_llave)
            if exito:
                messagebox.showinfo("Éxito", "El alumno ha sido removido y la lista se ha reordenado secuencialmente.")
                self.cargar_estudiantes_por_grado(grado_actual)
                
                # Sincronización directa con el Excel si es Directora/Admin
                if self.rol in ["Directora", "Administrativo"]:
                    sinc = messagebox.askyesno("Sincronizar", "¿Desea reescribir e impactar esta eliminación directamente en el Excel oficial?")
                    if sinc:
                        ok, msg_ex = migrar_excel.actualizar_excel_desde_csv(grado_actual)
                        if ok: messagebox.showinfo("Excel Sincronizado", msg_ex)
                        else: messagebox.showerror("Error Excel", msg_ex)
            else:
                messagebox.showerror("Error", msg)

    def mostrar_solo_lectura_representante(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado: return
        
        valores = self.tabla.item(item_seleccionado)['values']
        nombre_est = valores[3]
        datos_est = self.df_actual[self.df_actual['Estudiante'] == nombre_est].iloc[0]
        
        edad_actual = migrar_excel.calcular_edad(
            datos_est.get('Dia_Nac', 0), datos_est.get('Mes_Nac', 0), datos_est.get('Anio_Nac', 0)
        )
        
        top = ctk.CTkToplevel(self)
        top.title(f"Información Institucional - {nombre_est}")
        top.geometry("500x540")
        top.resizable(False, False)
        top.attributes("-topmost", True)

        ctk.CTkLabel(top, text="Ficha Informativa del Estudiante", font=("Helvetica", 16, "bold"), text_color="#1f538d").pack(pady=(15, 5))
        frame_est = ctk.CTkFrame(top)
        frame_est.pack(fill="x", padx=20, pady=5)
        
        txt_estudiante = (
            f"• Estudiante: {datos_est.get('Estudiante', '')}\n"
            f"• Cédula Identidad / Escolar: {valores[2]} / {valores[1]}\n"
            f"• Género: {datos_est.get('Genero', '')}\n"
            f"• Fecha de Nacimiento: {datos_est.get('Fecha de nacimiento', '')}\n"
            f"• Edad Actual: {edad_actual} 📅\n"
            f"• Lugar de Nacimiento: {datos_est.get('Lugar de Nacimiento', '')}"
        )
        ctk.CTkLabel(frame_est, text=txt_estudiante, justify="left", font=("Helvetica", 12)).pack(padx=15, pady=10, anchor="w")

        ctk.CTkLabel(top, text="Datos del Representante Legal", font=("Helvetica", 16, "bold"), text_color="#1a6332").pack(pady=(15, 5))
        frame_rep = ctk.CTkFrame(top)
        frame_rep.pack(fill="x", padx=20, pady=5)

        txt_repr = (
            f"• Nombre Completo: {datos_est.get('Representante', '')}\n"
            f"• Cédula de Identidad: {datos_est.get('Cédula', 'No registra')}\n"
            f"• Parentesco con el Alumno: {datos_est.get('Parentesco', 'No registra')}\n"
            f"• Teléfono de Contacto: {datos_est.get('Contacto', 'No registra')}\n"
            f"• Dirección de Habitación: {datos_est.get('Dirección', 'No registra')}"
        )
        ctk.CTkLabel(frame_rep, text=txt_repr, justify="left", font=("Helvetica", 12)).pack(padx=15, pady=10, anchor="w")

        ctk.CTkButton(top, text="Entendido / Cerrar", fg_color="gray", hover_color="#555555", command=top.destroy).pack(pady=20)

    def mostrar_ventana_agregar(self):
        grado_actual = self.combo_grado.get()
        top = ctk.CTkToplevel(self)
        top.title(f"Añadir Nuevo Estudiante - {grado_actual}")
        top.geometry("560x580")
        top.resizable(False, False)
        top.attributes("-topmost", True)

        tabview = ctk.CTkTabview(top, width=520, height=440)
        tabview.pack(pady=10, padx=20)
        tab_alumno = tabview.add("Datos Estudiante")
        tab_repr = tabview.add("Datos Representante")

        # Inputs Alumno
        ctk.CTkLabel(tab_alumno, text="Nombres del Estudiante:").pack(anchor="w", padx=10, pady=2)
        entry_nom_est = ctk.CTkEntry(tab_alumno, width=400).pack(padx=10, pady=2)
        entry_nom_est = tab_alumno.winfo_children()[-1]

        ctk.CTkLabel(tab_alumno, text="Apellidos del Estudiante:").pack(anchor="w", padx=10, pady=2)
        entry_ape_est = ctk.CTkEntry(tab_alumno, width=400).pack(padx=10, pady=2)
        entry_ape_est = tab_alumno.winfo_children()[-1]

        ctk.CTkLabel(tab_alumno, text="Cédula Escolar (Opcional):").pack(anchor="w", padx=10, pady=2)
        entry_ced_esc = ctk.CTkEntry(tab_alumno, width=400).pack(padx=10, pady=2)
        entry_ced_esc = tab_alumno.winfo_children()[-1]

        ctk.CTkLabel(tab_alumno, text="Cédula Identidad (Opcional):").pack(anchor="w", padx=10, pady=2)
        entry_ced_id = ctk.CTkEntry(tab_alumno, width=400).pack(padx=10, pady=2)
        entry_ced_id = tab_alumno.winfo_children()[-1]

        ctk.CTkLabel(tab_alumno, text="Lugar de Nacimiento:").pack(anchor="w", padx=10, pady=2)
        entry_lugar = ctk.CTkEntry(tab_alumno, width=400).pack(padx=10, pady=2)
        entry_lugar = tab_alumno.winfo_children()[-1]

        frame_fecha = ctk.CTkFrame(tab_alumno, fg_color="transparent")
        frame_fecha.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(frame_fecha, text="Día:").grid(row=0, column=0, padx=2)
        entry_dia = ctk.CTkEntry(frame_fecha, width=40); entry_dia.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_fecha, text="Mes:").grid(row=0, column=2, padx=2)
        entry_mes = ctk.CTkEntry(frame_fecha, width=40); entry_mes.grid(row=0, column=3, padx=5)
        ctk.CTkLabel(frame_fecha, text="Año:").grid(row=0, column=4, padx=2)
        entry_anio = ctk.CTkEntry(frame_fecha, width=60); entry_anio.grid(row=0, column=5, padx=5)

        ctk.CTkLabel(tab_alumno, text="Género (M/F):").pack(anchor="w", padx=10, pady=2)
        entry_genero = ctk.CTkEntry(tab_alumno, width=80).pack(anchor="w", padx=10, pady=2)
        entry_genero = tab_alumno.winfo_children()[-1]

        # Inputs Representante
        ctk.CTkLabel(tab_repr, text="Nombres del Representante:").pack(anchor="w", padx=10, pady=2)
        entry_nom_rep = ctk.CTkEntry(tab_repr, width=400).pack(padx=10, pady=2)
        entry_nom_rep = tab_repr.winfo_children()[-1]

        ctk.CTkLabel(tab_repr, text="Apellidos del Representante:").pack(anchor="w", padx=10, pady=2)
        entry_ape_rep = ctk.CTkEntry(tab_repr, width=400).pack(padx=10, pady=2)
        entry_ape_rep = tab_repr.winfo_children()[-1]

        ctk.CTkLabel(tab_repr, text="Cédula de Identidad:").pack(anchor="w", padx=10, pady=2)
        entry_ced_rep = ctk.CTkEntry(tab_repr, width=400).pack(padx=10, pady=2)
        entry_ced_rep = tab_repr.winfo_children()[-1]

        ctk.CTkLabel(tab_repr, text="Contacto Telefónico:").pack(anchor="w", padx=10, pady=2)
        entry_tlf_rep = ctk.CTkEntry(tab_repr, width=400).pack(padx=10, pady=2)
        entry_tlf_rep = tab_repr.winfo_children()[-1]

        ctk.CTkLabel(tab_repr, text="Parentesco:").pack(anchor="w", padx=10, pady=2)
        entry_par_rep = ctk.CTkEntry(tab_repr, width=400).pack(padx=10, pady=2)
        entry_par_rep = tab_repr.winfo_children()[-1]

        ctk.CTkLabel(tab_repr, text="Dirección Completa:").pack(anchor="w", padx=10, pady=2)
        entry_dir_rep = ctk.CTkEntry(tab_repr, width=400).pack(padx=10, pady=2)
        entry_dir_rep = tab_repr.winfo_children()[-1]

        def guardar_nuevo_alumno():
            if not entry_nom_est.get().strip() or not entry_ape_est.get().strip():
                messagebox.showwarning("Campos Requeridos", "El nombre y apellido del estudiante son campos obligatorios.")
                return
                
            dic_est = {
                'Cédula Escolar': entry_ced_esc.get().strip() or "No posee",
                'Cédula Identidad': entry_ced_id.get().strip() or "No posee",
                'Nombres_Est': entry_nom_est.get().strip(),
                'Apellidos_Est': entry_ape_est.get().strip(),
                'Lugar de Nacimiento': entry_lugar.get().strip(),
                'Dia_Nac': entry_dia.get().strip(),
                'Mes_Nac': entry_mes.get().strip(),
                'Anio_Nac': entry_anio.get().strip(),
                'Genero': entry_genero.get().strip().upper()
            }
            dic_rep = {
                'Repr_Nombre': entry_nom_rep.get().strip(),
                'Repr_Apellido': entry_ape_rep.get().strip(),
                'Cédula': entry_ced_rep.get().strip(),
                'Contacto': entry_tlf_rep.get().strip(),
                'Parentesco': entry_par_rep.get().strip(),
                'Dirección': entry_dir_rep.get().strip()
            }
            
            exito, msg = migrar_excel.agregar_estudiante_en_csv(grado_actual, dic_est, dic_rep)
            if exito:
                messagebox.showinfo("Éxito", "Estudiante anexado a la base de datos CSV de forma correcta.")
                self.cargar_estudiantes_por_grado(grado_actual)
                
                if self.rol in ["Directora", "Administrativo"]:
                    sinc_excel = messagebox.askyesno("Sincronizar", "¿Desea inyectar este nuevo alumno directo al Excel oficial (.xlsx) de este grado?")
                    if sinc_excel:
                        ok_ex, msg_ex = migrar_excel.actualizar_excel_desde_csv(grado_actual)
                        if ok_ex: messagebox.showinfo("Excel Sincronizado", msg_ex)
                        else: messagebox.showerror("Error Excel", msg_ex)
                top.destroy()
            else:
                messagebox.showerror("Error", msg)

        btn_crear = ctk.CTkButton(top, text="➕ Agregar Alumno Oficial", fg_color="#1a6332", command=guardar_nuevo_alumno)
        btn_crear.pack(pady=15)

    def mostrar_detalle_y_edicion(self):
        item_seleccionado = self.tabla.selection()
        if not item_seleccionado: return
        
        valores = self.tabla.item(item_seleccionado)['values']
        nombre_est = valores[3]
        
        datos_est = self.df_actual[self.df_actual['Estudiante'] == nombre_est].iloc[0]
        cedula_llave = datos_est['Cédula Identidad'] if datos_est['Cédula Identidad'] != "No posee" else datos_est['Cédula Escolar']
        grado_actual = self.combo_grado.get()

        top = ctk.CTkToplevel(self)
        top.title(f"Ficha Completa de {nombre_est}")
        top.geometry("560x580")
        top.resizable(False, False)
        top.attributes("-topmost", True)

        tabview = ctk.CTkTabview(top, width=520, height=440)
        tabview.pack(pady=10, padx=20)
        tab_alumno = tabview.add("Datos Estudiante")
        tab_repr = tabview.add("Datos Representante")

        # Inputs Edición Alumno
        ctk.CTkLabel(tab_alumno, text="Nombres del Estudiante:").pack(anchor="w", padx=10, pady=2)
        entry_nom_est = ctk.CTkEntry(tab_alumno, width=400)
        entry_nom_est.insert(0, datos_est.get('Nombres_Est', ''))
        entry_nom_est.pack(padx=10, pady=2)

        ctk.CTkLabel(tab_alumno, text="Apellidos del Estudiante:").pack(anchor="w", padx=10, pady=2)
        entry_ape_est = ctk.CTkEntry(tab_alumno, width=400)
        entry_ape_est.insert(0, datos_est.get('Apellidos_Est', ''))
        entry_ape_est.pack(padx=10, pady=2)

        ctk.CTkLabel(tab_alumno, text="Lugar de Nacimiento:").pack(anchor="w", padx=10, pady=2)
        entry_lugar = ctk.CTkEntry(tab_alumno, width=400)
        entry_lugar.insert(0, datos_est.get('Lugar de Nacimiento', ''))
        entry_lugar.pack(padx=10, pady=2)

        frame_fecha = ctk.CTkFrame(tab_alumno, fg_color="transparent")
        frame_fecha.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(frame_fecha, text="Día:").grid(row=0, column=0, padx=2)
        entry_dia = ctk.CTkEntry(frame_fecha, width=40); entry_dia.insert(0, datos_est.get('Dia_Nac', '')); entry_dia.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_fecha, text="Mes:").grid(row=0, column=2, padx=2)
        entry_mes = ctk.CTkEntry(frame_fecha, width=40); entry_mes.insert(0, datos_est.get('Mes_Nac', '')); entry_mes.grid(row=0, column=3, padx=5)
        ctk.CTkLabel(frame_fecha, text="Año:").grid(row=0, column=4, padx=2)
        entry_anio = ctk.CTkEntry(frame_fecha, width=60); entry_anio.insert(0, datos_est.get('Anio_Nac', '')); entry_anio.grid(row=0, column=5, padx=5)

        ctk.CTkLabel(tab_alumno, text="Género (M/F):").pack(anchor="w", padx=10, pady=2)
        entry_genero = ctk.CTkEntry(tab_alumno, width=80)
        entry_genero.insert(0, datos_est.get('Genero', ''))
        entry_genero.pack(anchor="w", padx=10, pady=2)

        # Inputs Edición Representante
        ctk.CTkLabel(tab_repr, text="Nombres del Representante:").pack(anchor="w", padx=10, pady=2)
        entry_nom_rep = ctk.CTkEntry(tab_repr, width=400)
        entry_nom_rep.insert(0, datos_est.get('Repr_Nombre', ''))
        entry_nom_rep.pack(padx=10, pady=2)

        ctk.CTkLabel(tab_repr, text="Apellidos del Representante:").pack(anchor="w", padx=10, pady=2)
        entry_ape_rep = ctk.CTkEntry(tab_repr, width=400)
        entry_ape_rep.insert(0, datos_est.get('Repr_Apellido', ''))
        entry_ape_rep.pack(padx=10, pady=2)

        ctk.CTkLabel(tab_repr, text="Cédula de Identidad:").pack(anchor="w", padx=10, pady=2)
        entry_ced_rep = ctk.CTkEntry(tab_repr, width=400)
        entry_ced_rep.insert(0, datos_est.get('Cédula', ''))
        entry_ced_rep.pack(padx=10, pady=2)

        ctk.CTkLabel(tab_repr, text="Contacto Telefónico:").pack(anchor="w", padx=10, pady=2)
        entry_tlf_rep = ctk.CTkEntry(tab_repr, width=400)
        entry_tlf_rep.insert(0, datos_est.get('Contacto', ''))
        entry_tlf_rep.pack(padx=10, pady=2)

        ctk.CTkLabel(tab_repr, text="Parentesco:").pack(anchor="w", padx=10, pady=2)
        entry_par_rep = ctk.CTkEntry(tab_repr, width=400)
        entry_par_rep.insert(0, datos_est.get('Parentesco', ''))
        entry_par_rep.pack(padx=10, pady=2)

        ctk.CTkLabel(tab_repr, text="Dirección Completa:").pack(anchor="w", padx=10, pady=2)
        entry_dir_rep = ctk.CTkEntry(tab_repr, width=400)
        entry_dir_rep.insert(0, datos_est.get('Dirección', ''))
        entry_dir_rep.pack(padx=10, pady=2)

        def guardar_cambios_locales():
            dic_est = {
                'Nombres_Est': entry_nom_est.get().strip(),
                'Apellidos_Est': entry_ape_est.get().strip(),
                'Lugar de Nacimiento': entry_lugar.get().strip(),
                'Dia_Nac': entry_dia.get().strip(),
                'Mes_Nac': entry_mes.get().strip(),
                'Anio_Nac': entry_anio.get().strip(),
                'Genero': entry_genero.get().strip().upper()
            }
            dic_rep = {
                'Repr_Nombre': entry_nom_rep.get().strip(),
                'Repr_Apellido': entry_ape_rep.get().strip(),
                'Cédula': entry_ced_rep.get().strip(),
                'Contacto': entry_tlf_rep.get().strip(),
                'Parentesco': entry_par_rep.get().strip(),
                'Dirección': entry_dir_rep.get().strip()
            }
            
            exito, msg = migrar_excel.modificar_datos_en_csv(grado_actual, cedula_llave, dic_est, dic_rep)
            if exito:
                messagebox.showinfo("Éxito", "Los cambios han sido aplicados al archivo CSV.")
                self.cargar_estudiantes_por_grado(grado_actual)
                
                if self.rol in ["Directora", "Administrativo"]:
                    sinc_excel = messagebox.askyesno("Sincronizar", "¿Desea actualizar y exportar estos cambios directamente al Excel oficial (.xlsx) de este grado?")
                    if sinc_excel:
                        ok_ex, msg_ex = migrar_excel.actualizar_excel_desde_csv(grado_actual)
                        if ok_ex: messagebox.showinfo("Excel Sincronizado", msg_ex)
                        else: messagebox.showerror("Error Excel", msg_ex)
                top.destroy()
            else:
                messagebox.showerror("Error", msg)

        btn_guardar_cambios = ctk.CTkButton(top, text="💾 Guardar Cambios e Inyectar Datos", fg_color="#1f538d", command=guardar_cambios_locales)
        btn_guardar_cambios.pack(pady=15)


# ==========================================
# 3. VENTANA MAESTRA ÚNICA
# ==========================================
class AppEscuela(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión - U.E. Juana Ramírez")
        self.geometry("1100x650")
        self.resizable(True, True)

        self.after(50, lambda: self.state('zoomed'))
        self.frame_actual = None
        self.mostrar_pantalla_login()

    def mostrar_pantalla_login(self):
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        self.frame_actual = FrameLogin(self, callback_login_exitoso=self.mostrar_pantalla_dashboard)
        self.frame_actual.pack(fill="both", expand=True)

    def mostrar_pantalla_dashboard(self, nombre, rol):
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        self.frame_actual = FrameMenuPrincipal(self, nombre, rol, callback_cerrar_sesion=self.mostrar_pantalla_login)
        self.frame_actual.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AppEscuela()
    app.mainloop()