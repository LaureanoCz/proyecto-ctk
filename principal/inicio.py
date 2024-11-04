import sqlite3
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from principal import menu_principal
import config

showing_password = False

# -> --------------| Registration Form |-------------- <-
def register_form():
    # -> -------| Configuracion de la base de datos :) |------- <-
    conn = sqlite3.connect("datos.db")

    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        contraseña TEXT NOT NULL,
                        correo TEXT NOT NULL
                    )''')

    conn.commit()

    def mostrar_tabla():
        cursor.execute("SELECT * FROM usuarios")
        results = cursor.fetchall()
        
        results_df = pd.DataFrame(results, columns=["ID", "nombre", "contraseña", "correo"])
        print("\nTabla de usuarios:\n", results_df)

    def crear_cuenta():
        nombre = name_entry.get()
        contraseña = password_entry.get()
        correo = email_entry.get()
        confirm_contraseña = confirm_password_entry.get() 

        if '@' not in correo:
            messagebox.showwarning("Advertencia", "El correo electrónico debe contener '@'.")
            return

        if nombre and contraseña and correo:
            if contraseña != confirm_contraseña:
                messagebox.showwarning("Advertencia", "Las contraseñas no coinciden.")
                return
            
            cursor.execute("SELECT nombre FROM usuarios WHERE nombre = ? OR correo = ?", (nombre, correo))
            resultado = cursor.fetchone()

            if resultado:
                messagebox.showwarning("Advertencia", "El nombre o el correo ya están registrados.")
            else:
                cursor.execute("INSERT INTO usuarios (nombre, contraseña, correo) VALUES (?, ?, ?)", (nombre, contraseña, correo))
                conn.commit()
                conn.close()

                messagebox.showinfo("Éxito", "Datos guardados correctamente.")
                mostrar_tabla()
                switch_to_login(form_r)

                name_entry.delete(0, "end")
                password_entry.delete(0, "end")
                confirm_password_entry.delete(0, "end")
                email_entry.delete(0, "end")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")

    forml.destroy()
    
    global form_r
    form_r = ctk.CTk()
    form_r.title("EasyForms")
    
    # -> -------| Window Configuration |------- <-
    width = 420
    height = 650
    form_r.geometry(f"{width}x{height}")
    screen_width = form_r.winfo_screenwidth()
    screen_height = form_r.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    form_r.geometry(f"{width}x{height}+{x}+{y}")
    form_r.maxsize(420, 580)
    form_r.minsize(420, 580)
    form_r.iconbitmap("images/logo.ico")
    
    # -> -------| Frames |------- <-
    title = ctk.CTkFrame(form_r, fg_color="transparent", height=50, width=420)
    title.pack(pady=20)
    
    form_frame = ctk.CTkFrame(form_r, fg_color="transparent", height=580)
    form_frame.pack(fill="x", padx=10, pady=10)
    
    # -> -------| Password Toggle Function |------- <-
    eye_closed_image = Image.open("images/eye-off.png")
    eye_closed = ctk.CTkImage(eye_closed_image)

    eye_image = Image.open("images/eye.png")
    eye_open = ctk.CTkImage(eye_image)

    def toggle_password():
        global showing_password
        showing_password = not showing_password
        if showing_password:
            show_button.configure(image=eye_closed)
            password_entry.configure(show='')
            confirm_password_entry.configure(show='')
            show_button.configure(text="Hide Password")
        else:
            show_button.configure(image=eye_open)
            password_entry.configure(show='*')
            confirm_password_entry.configure(show='*')
            show_button.configure(text="Show Password")

    # -> -------| Elements [inputs, labels, etc.] |------- <-
    title1 = ctk.CTkLabel(title, text="Register", font=("Arial", 50))
    title1.pack(fill="x", padx=10, pady=10)
    
    name_entry = ctk.CTkEntry(form_frame, placeholder_text="Name", font=("Arial", 20), corner_radius=20)
    name_entry.pack(side="top", fill="x", pady="10")
    
    email_entry = ctk.CTkEntry(form_frame, placeholder_text="Email", font=("Arial", 20), corner_radius=20)
    email_entry.pack(side="top", fill="x", pady="10")
    
    password_entry = ctk.CTkEntry(form_frame, placeholder_text="Password", font=("Arial", 20), show="*", corner_radius=20)
    password_entry.pack(side="top", fill="x", pady="10")
    
    confirm_password_entry = ctk.CTkEntry(form_frame, placeholder_text="Confirm Password", font=("Arial", 20), show="*", corner_radius=20)
    confirm_password_entry.pack(side="top", fill="x", pady="10")
    
    show_button = ctk.CTkButton(form_frame, text="Show Password", image=eye_open, fg_color="transparent", compound="left", hover="false", command=toggle_password)
    show_button.pack(side="top", anchor="w")
    
    register_button = ctk.CTkButton(form_frame, text="Create Account", command=crear_cuenta, font=("Arial", 25, "bold"), corner_radius=10)
    register_button.pack(side="top", fill="x", pady="30", padx="30")
    
    login_label = ctk.CTkLabel(form_r, text="Already have an account?", width=420, font=("Arial", 15))
    login_label.pack(pady=10)
    
    login_button = ctk.CTkButton(form_r, text="Log in here", font=("Arial", 15), command=lambda: switch_to_login(form_r))
    login_button.pack(pady=10)
    
    form_r.mainloop()

# -> --------------| Function to Switch Windows |-------------- <-
def switch_to_login(form_r):
    form_r.destroy()
    login_form()


# -> --------------| Login Form |-------------- <-
def login_form():
    # -> -------| Configuracion de la base de datos :) |------- <-
    conn = sqlite3.connect("datos.db")
    cursor = conn.cursor()

    def iniciar_sesion():
        nombre = name_login.get()
        correo = email_login.get()
        contraseña = password_login.get()

        if '@' not in correo:
            messagebox.showwarning("Advertencia", "El correo electrónico debe contener '@'.")
            return

        if nombre and correo and contraseña:
            cursor.execute("SELECT nombre FROM usuarios WHERE nombre = ? AND correo = ? AND contraseña = ?", (nombre, correo, contraseña))
            resultado = cursor.fetchone()
            
            if resultado:
                config.nombre_usuario = nombre
                forml.destroy()
                conn.close()
                menu_principal()
            else:
                messagebox.showwarning("Advertencia", "El nombre, correo o la contraseña no son correctos.")
                name_login.delete(0, "end")
                password_login.delete(0, "end")
                email_login.delete(0, "end")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")

    global forml
    forml = ctk.CTk()
    forml.title("EasyForms")
    
    # -> -------| Window Configuration |------- <-
    width = 420
    height = 650
    forml.geometry(f"{width}x{height}")
    screen_width = forml.winfo_screenwidth()
    screen_height = forml.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    forml.geometry(f"{width}x{height}+{x}+{y}")
    forml.maxsize(420, 580)
    forml.minsize(420, 580)
    forml.iconbitmap("images/logo.ico")

    # -> -------| Password Toggle Function |------- <-
    eye_closed_image = Image.open("images/eye-off.png")
    eye_closed = ctk.CTkImage(eye_closed_image)

    eye_image = Image.open("images/eye.png")
    eye_open = ctk.CTkImage(eye_image)
    
    def toggle_password_login():
        global showing_password
        showing_password = not showing_password
        if showing_password:
            show_button_login.configure(image=eye_closed)
            password_login.configure(show='')
            show_button_login.configure(text="Hide Password")
        else:
            show_button_login.configure(image=eye_open)
            password_login.configure(show='*')
            show_button_login.configure(text="Show Password")

    # -> -------| Frames |------- <-
    title_frame = ctk.CTkFrame(forml, fg_color="transparent", height=50, width=420)
    title_frame.pack(pady=20)
    
    form_frame = ctk.CTkFrame(forml, fg_color="transparent", height=580)
    form_frame.pack(fill="x", padx=10, pady=10)
    
    title_label = ctk.CTkLabel(title_frame, text="Login", font=("Arial", 50))
    title_label.pack()
    
    # -> -------| Elements [inputs, labels, etc.] |------- <-
    name_login = ctk.CTkEntry(form_frame, placeholder_text="Name", font=("Arial", 20), corner_radius=20)
    name_login.pack(side="top", fill="x", pady="10")
    
    email_login = ctk.CTkEntry(form_frame, placeholder_text="Email", font=("Arial", 20), corner_radius=20)
    email_login.pack(side="top", fill="x", pady="10")
    
    password_login = ctk.CTkEntry(form_frame, placeholder_text="Password", font=("Arial", 20), show="*", corner_radius=20)
    password_login.pack(side="top", fill="x", pady="10")
    
    show_button_login = ctk.CTkButton(form_frame, text="Show Password", image=eye_open, fg_color="transparent", compound="left", hover="false", command=toggle_password_login)
    show_button_login.pack(side="top", anchor="w")
    
    login_button = ctk.CTkButton(form_frame, text="Login", command=iniciar_sesion,font=("Arial", 25, "bold"), corner_radius=10)
    login_button.pack(side="top", fill="x", pady="30", padx="30")

    auth_frame = ctk.CTkFrame(forml, fg_color="transparent", height=50)
    auth_frame.pack()
    
    google_icon = Image.open("images/google.png")
    google = ctk.CTkImage(google_icon, size=(25, 25))
    
    github_icon = Image.open("images/github.png")
    github = ctk.CTkImage(github_icon, size=(25, 25))
    
    google_button = ctk.CTkButton(auth_frame, image=google, text="Google", font=("Arial", 25), fg_color="white", hover_color="#f0f0f0", border_width=2, border_color="black", corner_radius=10, text_color="black")
    google_button.pack(side="left", padx=15)
    
    github_button = ctk.CTkButton(auth_frame, image=github, text="GitHub", font=("Arial", 25), fg_color="#181717", hover_color="#121212", border_width=2, border_color="black", corner_radius=10, text_color="white")
    github_button.pack(side="left", padx=15)
    
    register_label = ctk.CTkLabel(forml, text="Don't have an account yet?", width=420, font=("Arial", 15))
    register_label.pack(pady=30)
    
    register_button = ctk.CTkButton(forml, text="Register here", font=("Arial", 15), command=lambda: register_form())
    register_button.pack(pady=10)
    
    forml.mainloop()