import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import config

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -> --------------| Prueba del menu principal de la aplicacion |-------------- <-

def menu_principal():
    # -> -------| Images |------- <-
    search_icon_image = Image.open("images/search.png")
    search_icon = ctk.CTkImage(search_icon_image)

    user_photo_image = Image.open("images/user.png")
    user_photo = ctk.CTkImage(user_photo_image, size=(80, 80))

    menu = ctk.CTk()
    menu.title("EasyForms")

    # -> -------| Window Configuration |------- <- 
    width = 1000
    height = 500
    menu.geometry(f"{width}x{height}")
        
    screen_width = menu.winfo_screenwidth()
    screen_height = menu.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    menu.geometry(f"{width}x{height}+{x}+{y}")
        
    menu.maxsize(1000, 500)
    menu.minsize(1000, 500)
    menu.iconbitmap("images/logo.ico")

    # -> -------| Frames |------- <-
    nav_frame = ctk.CTkFrame(menu, width=1000, height=50)
    nav_frame.grid(column=0, row=0, columnspan=3)
    nav_frame.grid_propagate(False)

    nav_frame.grid_columnconfigure(0, weight=0)  # Espacio a la izquierda
    nav_frame.grid_columnconfigure(1, weight=1)  # Columna del botón
    nav_frame.grid_columnconfigure(2, weight=1)  # Espacio entre botón y entry
    nav_frame.grid_columnconfigure(3, weight=0)  # Columna del entry # Espacio a la derecha

    user_info_frame = ctk.CTkFrame(menu, width=150, height=400)
    user_info_frame.grid(column=0, row=1, pady=25, padx=5)
    user_info_frame.grid_propagate(False)

    forms_frame = ctk.CTkFrame(menu, width=800, height=400)
    forms_frame.grid(column=1, row=1, columnspan=4, padx=20, pady=25)

    # -> -------| Frames de los formularios | ------- <-
    form_one_frame = ctk.CTkFrame(forms_frame, width=250, height=190)
    form_one_frame.grid(column=0, row=0, pady=2.5, padx=2.5)

    form_two_frame = ctk.CTkFrame(forms_frame, width=250, height=190)
    form_two_frame.grid(column=0, row=1, pady=2.5, padx=2.5)

    form_three_frame = ctk.CTkFrame(forms_frame, width=250, height=190)
    form_three_frame.grid(column=1, row=0, pady=2.5, padx=2.5)

    form_four_frame = ctk.CTkFrame(forms_frame, width=250, height=190)
    form_four_frame.grid(column=1, row=1, pady=2.5, padx=2.5)

    form_five_frame = ctk.CTkFrame(forms_frame, width=250, height=190)
    form_five_frame.grid(column=2, row=0, pady=2.5, padx=2.5)

    form_six_frame = ctk.CTkFrame(forms_frame, width=250, height=190)
    form_six_frame.grid(column=2, row=1, pady=2.5, padx=2.5)

    # -> -------| Elements [inputs, labels, etc.] *(NAV)* |------- <-
    make_form_button = ctk.CTkButton(nav_frame, text="Create form", font=("Arial", 15), height=30)
    make_form_button.grid(column=0, row=0, pady=5, padx=15)

    nav_entry = ctk.CTkEntry(nav_frame, height=40, width=350, justify="center", placeholder_text="Search for a form", font=("Arial", 15), border_width=0)
    nav_entry.grid(column=3, row=0, columnspan=2, pady=5)

    search_icon_button = ctk.CTkButton(nav_frame, image=search_icon, text='', width=50, height=30, fg_color="transparent", hover=None)
    search_icon_button.grid(column=5, row=0, padx=10)

     # -> -------| Elements [inputs, labels, etc.] *(User info)* |------- <-
    user_photo = ctk.CTkLabel(user_info_frame, image=user_photo, text="")
    user_photo.pack(padx=35)

    name_label = ctk.CTkLabel(user_info_frame, text=config.nombre_usuario)
    name_label.pack()

    menu.mainloop()