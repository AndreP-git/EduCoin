import tkinter as tk
import time, os, sys
    
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
        self.title.pack()
        
        # Canvas
        self.canvas = tk.Canvas(self.master, width=900, height=550, background='gray75')
        self.canvas.pack(pady=10)
        
        # Miner
        self.miner_label = tk.Label(self.canvas, text='Miner')
        self.miner_win = self.canvas.create_window(20, 30, anchor='nw', window=self.miner_label)
        
        # Miner --> WhileTRUE
        self.canvas.create_line(40, 40, 100, 40, arrow="last")
        
        # WhileTRUE
        self.while_label = tk.Label(self.canvas, text='While TRUE:')
        self.while_win = self.canvas.create_window(100, 30, anchor='nw', window=self.while_label)
        
        # WhileTRUE --> GetLast
        self.canvas.create_line(135, 30, 135, 80, arrow="last")
        
        # GetLast
        self.getLast_label = tk.Label(self.canvas, text='Get last block and its\n"Proof of work"')
        self.getLast_win = self.canvas.create_window(75, 80, anchor='nw', window=self.getLast_label)
        
        # GetLast --> Find
        self.canvas.create_line(135, 80, 135, 150, arrow="last")
        
        # Find
        self.find_label = tk.Label(self.canvas, text='Find "Proof of Work"\nof the current block')
        self.find_win = self.canvas.create_window(75, 150, anchor='nw', window=self.find_label)
        
        # Find --> Other
        self.canvas.create_line(135, 150, 135, 220, arrow="last")
        
        # Other choice
        self.other_label = tk.Label(self.canvas, text='Other nodes\nfound proof')
        self.other_win = self.canvas.create_window(100, 220, anchor='nw', window=self.other_label)
        
        # Other --> Create
        self.canvas.create_line(135, 220, 135, 290, arrow="last")
        
        # Create mining transaction
        self.create_label = tk.Label(self.canvas, text='Create a mining reward\ntansaction, add it to\npending transactions')
        self.create_win = self.canvas.create_window(75, 290, anchor='nw', window=self.create_label)
        
        # Create --> New
        self.canvas.create_line(135, 290, 135, 370, arrow="last")
        
        # New Block
        self.newBlock_label = tk.Label(self.canvas, text='Create a new block\nwith all pending\n transactions')
        self.newBlock_win = self.canvas.create_window(85, 370, anchor='nw', window=self.newBlock_label)
        
        # New --> Add
        self.canvas.create_line(135, 370, 135, 450, arrow="last")
        
        # Add new block
        self.add_label = tk.Label(self.canvas, text='Add the new block to\nthe chain')
        self.add_win = self.canvas.create_window(80, 450, anchor='nw', window=self.add_label)
        
        # ------- 2nd route --------
        
        # Other --> Update
        self.canvas.create_line(100, 235, 230, 235, arrow="last")
        
        # Update blockchain
        self.update_label = tk.Label(self.canvas, text='Update blockchain\nwith verified block')
        self.update_win = self.canvas.create_window(230, 220, anchor='nw', window=self.update_label)

        # Back to whileTRUE
        self.canvas.create_line(280, 250, 280, 40, 170, 40, arrow="last")
        
        # ------- feedback --------
        self.canvas.create_line(135, 450, 135, 510, 400, 510, 400, 20, 135, 20, 135, 30, arrow="last")
       
if __name__ == '__main__':
    
    # Start miner GUI
    root = tk.Tk()
    root.title("EduCoin")
    root.geometry("1000x750")
    miner = Miner(master=root)
    miner.mainloop()