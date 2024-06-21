import customtkinter as ctk
import query_scraping as qs
import webbrowser
# Necessary imports.

class ResultFrame(ctk.CTkFrame):
    def __init__(self, parent, results):
        super().__init__(parent)
        self.configure(fg_color='#89a1c7',
                       border_width=0,
                       corner_radius=0)

        self.results = results
        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        ctk.CTkLabel(self,
                     text=f'{self.results[0]}',
                     font=('Lucida Grande', 30),
                     wraplength=325).grid(column=0, row=0, sticky='news')

        ctk.CTkLabel(self,
                     text=f'{self.results[2]}',
                     font=('Lucida Grande', 13),
                     wraplength=325).grid(column=0, row=1, sticky='news')

        ctk.CTkLabel(self,
                     text=f'{self.results[3]}',
                     font=('Lucida Grande', 18),
                     wraplength=325).grid(column=1, row=0, rowspan=2, sticky='news')

        ctk.CTkButton(self,
                      text=f'Go to page',
                      font=('Lucida Grande', 20),
                      fg_color='#3e289c',
                      hover_color='#2e2670',
                      command=lambda:webbrowser.open(self.results[1])).grid(column=2, row=0, rowspan=2, sticky='news', padx=20, pady=20)

        self.pack(expand=True, fill='both')
    # Makes the frames to display the information that has been scraped from wikipedia, and inserts it into a scrollable frame.

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1000x1000')
        self.title('Convenient Wiki Search')
        self.resizable(False, False)
        self.holding_frame = ctk.CTkScrollableFrame(self)
        self.searchframe()
        self.mainloop()
    # Initialises and launches the main application.

    def searchframe(self):
        self.search_frame = ctk.CTkFrame(self,
                                         fg_color='#89a1c7',
                                         border_width=5,
                                         border_color='#7185a6',
                                         corner_radius=0)

        self.text = ctk.StringVar()
        self.text_bar = ctk.CTkEntry(self.search_frame,
                                     placeholder_text='Insert text here',
                                     placeholder_text_color='#1a3452',
                                     font=('Lucida Grande', 45),
                                     text_color='#1a3452',
                                     corner_radius=0,
                                     border_width=0,
                                     fg_color='#537399')
        self.text_bar.pack(expand=True, fill='both', side='left', padx=5, pady=5)

        self.limit_amount = ctk.IntVar(value=5)
        self.limit = ctk.CTkSlider(self.search_frame,
                                   from_=5,
                                   to=100,
                                   variable=self.limit_amount,
                                   width=300,
                                   fg_color='#818ea3',
                                   progress_color='#415a82',
                                   button_color='#477fcc',
                                   button_hover_color='#28589c')
        self.limit.pack(expand=True, fill='x', padx=5)

        ctk.CTkLabel(self.search_frame,
                     text=f'Amount of results:',
                     font=('Lucida Grande', 18, 'bold'),
                     text_color='#3e289c').place(relx=0.745, rely=0.6)

        ctk.CTkLabel(self.search_frame,
                     textvariable=self.limit_amount,
                     font=('Lucida Grande', 18, 'bold'),
                     text_color='#3e289c').place(relx=0.92, rely=0.61)

        self.text_bar.bind('<Return>', lambda e: self.getting_results())

        self.search_frame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
    # Creates a bar at the top where the user can input text, and specify how many results they want.

    def results_frame(self):
        self.holding_frame = ctk.CTkScrollableFrame(self,
                                                    fg_color='#89a1c7',
                                                    corner_radius=0)
        result_list = qs.ScrapingWebsite(self.text_bar.get(), self.limit.get()).getting_results()
        for results in result_list:
            ResultFrame(self.holding_frame, results)

        self.holding_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
    # This takes the search and limit written in the input fields and uses it to get the scraped content from the site.
    # It loops through the list of data, using each to make an individual frame to display the title, etc.

    def getting_results(self):
        if self.holding_frame.winfo_exists() is True:
            self.holding_frame.destroy()
            self.results_frame()

        else:
            self.results_frame()
    # Checks if the frame to display data exists - if it does, it destroys what was there and re-creates the frame with
    # the updated query and limits. If it doesn't, it just runs the frame with the query and limits.

App()