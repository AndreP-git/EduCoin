import tkinter as tk
import time

class Miner(tk.Frame):
    
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master
        # self.pack(fill=tk.BOTH, expand=True)

        # Title label
        self.title = tk.Label(self.master, text="=============================\n" + 
          "Welcome to EduCoin!\n" + 
          f"Currently running: {os.path.basename(sys.argv[0])}\n" + 
          "=============================\n" +
          "Miner:\n")
        self.title["font"] = ("Arial", 16, "bold")
        self.title.pack(pady=10)
        
        # Canvas
        self.canvas = tk.Canvas(self.master, width=900, height=500, background='gray75')
        self.canvas.pack(pady=10)
        
        # Root
        #root_rect = canvas.create_rectangle(10, 10, 200, 50, fill='red', outline='blue', )
        self.root_label = tk.Label(self.canvas, text='Implode!')
        self.root_win = self.canvas.create_window(20, 20, anchor='nw', window=self.root_label)
        
        # Line root to pipe
        self.canvas.create_line(10, 10, 200, 50, arrow="last")
        
        # Setting update function
        self.canvas.after(5000, self.update)
        
    def update(self) -> None:
        self.root_label["bg"] = "red"
        time.sleep(1)
        self.root_label["bg"] = "blue"
        
if __name__ == '__main__':

    # Start miner GUI
    root = tk.Tk()
    root.title("EduCoin")
    root.geometry("1000x750")
    miner = Miner(master=root)
    miner.mainloop()