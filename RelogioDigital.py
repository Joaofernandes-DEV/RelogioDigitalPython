import tkinter as tk
from tkinter import ttk 
from datetime import datetime

class ProfessionalDigitalClock:
    def __init__(self, master):
        self.master = master
        master.title("Relógio Digital Profissional")
        master.geometry("800x400") # Tamanho inicial
        master.minsize(400, 200)   # Tamanho mínimo razoável
        master.configure(bg="#1a1a2e") 
        
        self._configure_colors_fonts()
        self._create_widgets()
        
        # Removida: self.colon_visible = True # Não é mais necessário para a animação

        # Bind o evento de redimensionamento da janela principal
        self.master.bind("<Configure>", self._on_window_resize)

        # Inicia a atualização do relógio
        self._update_clock()

    def _configure_colors_fonts(self):
        """Define as cores e fontes baseadas no exemplo HTML/CSS."""
        self.colors = {
            "bg_gradient_start": "#1a1a2e", 
            "bg_gradient_end": "#16213e",   
            "clock_face_bg": "#2A2A3E",     
            "clock_face_border": "#3A3A5E", 
            "time_text": "#FFFFFF",         
            "date_text_tk": "#CCCCCC", 
            "glow_color": "#00FFFF"         
        }

        self.font_family = "Orbitron" 
        # Tamanhos iniciais, serão ajustados dinamicamente
        self.time_font_size_base = 80  
        self.date_font_size_base = 20
        self.ampm_font_size_base = 20

    def _create_widgets(self):
        """Cria os elementos da interface do relógio."""
        self.gradient_canvas = tk.Canvas(
            self.master, 
            highlightthickness=0 
        )
        self.gradient_canvas.pack(expand=True, fill="both")
        
        self.clock_face_frame = tk.Frame(
            self.gradient_canvas,
            bg=self.colors["clock_face_bg"], 
            bd=1, 
            relief="solid", 
            highlightbackground=self.colors["clock_face_border"], 
            highlightthickness=1
        )
        
        # Frame para a hora e AM/PM (usando grid)
        self.time_display_frame = tk.Frame(self.clock_face_frame, bg=self.colors["clock_face_bg"])
        self.time_display_frame.pack(pady=(0, 20), expand=True) 

        self.hours_label = tk.Label(self.time_display_frame, text="00", 
                                    font=(self.font_family, self.time_font_size_base, "bold"), # Usar base aqui, será atualizado
                                    fg=self.colors["time_text"], bg=self.colors["clock_face_bg"])
        self.hours_label.grid(row=0, column=0)

        self.colon1_label = tk.Label(self.time_display_frame, text=":", 
                                     font=(self.font_family, self.time_font_size_base, "bold"), 
                                     fg=self.colors["time_text"], bg=self.colors["clock_face_bg"]) # Cor fixa
        self.colon1_label.grid(row=0, column=1)

        self.minutes_label = tk.Label(self.time_display_frame, text="00", 
                                      font=(self.font_family, self.time_font_size_base, "bold"), 
                                      fg=self.colors["time_text"], bg=self.colors["clock_face_bg"])
        self.minutes_label.grid(row=0, column=2)

        self.colon2_label = tk.Label(self.time_display_frame, text=":", 
                                     font=(self.font_family, self.time_font_size_base, "bold"), 
                                     fg=self.colors["time_text"], bg=self.colors["clock_face_bg"]) # Cor fixa
        self.colon2_label.grid(row=0, column=3)

        self.seconds_label = tk.Label(self.time_display_frame, text="00", 
                                      font=(self.font_family, self.time_font_size_base, "bold"), 
                                      fg=self.colors["time_text"], bg=self.colors["clock_face_bg"])
        self.seconds_label.grid(row=0, column=4)

        self.ampm_label = tk.Label(self.time_display_frame, text="AM", 
                                   font=(self.font_family, self.ampm_font_size_base), 
                                   fg=self.colors["date_text_tk"], bg=self.colors["clock_face_bg"])
        self.ampm_label.grid(row=0, column=5, sticky="se", padx=(10,0), pady=(0,10)) 

        self.date_label = tk.Label(self.clock_face_frame, text="Segunda-feira, 01 de Janeiro de 2023", 
                                   font=(self.font_family, self.date_font_size_base), 
                                   fg=self.colors["date_text_tk"], bg=self.colors["clock_face_bg"])
        self.date_label.pack(pady=(0, 0))

        # Inicializa o posicionamento e tamanhos dos elementos
        self._on_window_resize(None) # Chama uma vez para configurar o layout inicial

    def _on_window_resize(self, event):
        """
        Callback para o evento de redimensionamento da janela.
        Redesenha o gradiente, ajusta o tamanho das fontes e reposiciona o frame do relógio.
        """
        self.master.update_idletasks() 
        width = self.gradient_canvas.winfo_width()
        height = self.gradient_canvas.winfo_height()
        
        if width == 0 or height == 0:
            return 

        self._draw_gradient_background(width, height)
        self._update_font_sizes(width, height)
        self._update_clock_face_position(width, height)


    def _draw_gradient_background(self, width, height):
        """Desenha um gradiente linear no canvas para o fundo."""
        self.gradient_canvas.delete("gradient") 

        for i in range(height):
            r1, g1, b1 = self.master.winfo_rgb(self.colors["bg_gradient_start"])
            r2, g2, b2 = self.master.winfo_rgb(self.colors["bg_gradient_end"])
            
            r1, g1, b1 = r1//256, g1//256, b1//256
            r2, g2, b2 = r2//256, g2//256, b2//256

            ratio = i / height
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.gradient_canvas.create_line(0, i, width, i, fill=color, tags="gradient")
        
        if hasattr(self, 'clock_face_frame_id'): 
            self.gradient_canvas.tag_raise(self.clock_face_frame_id)

    def _update_font_sizes(self, width, height):
        """Ajusta os tamanhos das fontes com base nas dimensões da janela."""
        # A fonte será ~6.6% da largura da janela
        new_time_font_size = int(self.time_font_size_base * (width / 800)) 
        new_date_font_size = int(self.date_font_size_base * (width / 800))
        new_ampm_font_size = int(self.ampm_font_size_base * (width / 800))

        new_time_font_size = max(30, min(new_time_font_size, 150))
        new_date_font_size = max(10, min(new_date_font_size, 40))
        new_ampm_font_size = max(10, min(new_ampm_font_size, 40))

        self.hours_label.config(font=(self.font_family, new_time_font_size, "bold"))
        self.colon1_label.config(font=(self.font_family, new_time_font_size, "bold"))
        self.minutes_label.config(font=(self.font_family, new_time_font_size, "bold"))
        self.colon2_label.config(font=(self.font_family, new_time_font_size, "bold"))
        self.seconds_label.config(font=(self.font_family, new_time_font_size, "bold"))
        self.ampm_label.config(font=(self.font_family, new_ampm_font_size))
        self.date_label.config(font=(self.font_family, new_date_font_size))

    def _update_clock_face_position(self, canvas_width, canvas_height):
        """Atualiza a posição e o tamanho do clock_face_frame no centro do canvas."""
        
        frame_width = int(canvas_width * 0.9)
        
        self.clock_face_frame.update_idletasks() 
        frame_height = self.clock_face_frame.winfo_reqheight() 

        x_pos = canvas_width / 2
        y_pos = canvas_height / 2

        if not hasattr(self, 'clock_face_frame_id'):
            self.clock_face_frame_id = self.gradient_canvas.create_window(
                x_pos, y_pos, 
                window=self.clock_face_frame, anchor="center",
                width=frame_width 
            )
        else:
            self.gradient_canvas.coords(self.clock_face_frame_id, x_pos, y_pos)
            self.gradient_canvas.itemconfigure(self.clock_face_frame_id, width=frame_width)
        
        self.time_display_frame.pack_configure(expand=True)


    def _update_clock(self):
        """
        Atualiza a hora, data. Os dois pontos ficam fixos.
        """
        now = datetime.now()
        
        hours = now.strftime('%I') 
        minutes = now.strftime('%M')
        seconds = now.strftime('%S')
        ampm = now.strftime('%p') 
        
        self.hours_label.config(text=hours)
        self.minutes_label.config(text=minutes)
        self.seconds_label.config(text=seconds)
        self.ampm_label.config(text=ampm)

        # Removida a lógica do pisca-pisca dos dois pontos
        # self.colon_visible = not self.colon_visible
        # colon_color = self.colors["time_text"] if self.colon_visible else self.colors["clock_face_bg"]
        # self.colon1_label.config(fg=colon_color)
        # self.colon2_label.config(fg=colon_color)

        # Data (ex: Segunda-feira, 08 de Julho de 2025)
        # Lembre-se: O relógio está sendo executado em 8 de julho de 2025.
        weekday_map = {
            'Monday': 'Segunda-feira', 'Tuesday': 'Terça-feira', 'Wednesday': 'Quarta-feira',
            'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        month_map = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
        }
        
        day_of_week = now.strftime('%A')
        month_name = now.strftime('%B')
        
        date_str = f"{weekday_map.get(day_of_week, day_of_week)}, {now.day} de {month_map.get(month_name, month_name)} de {now.year}"
        self.date_label.config(text=date_str)
        
        self.master.after(1000, self._update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalDigitalClock(root)
    root.mainloop()