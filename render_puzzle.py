from PIL import Image, ImageTk
import tkinter as tk
import random
from RL import generate_random_state
# AI_Toggle=0
move = {0: 'up ', 1: 'down ', 2: 'left ', 3: 'right '}
class GameRenderer:
    
    def get_grid_position(self,grid_index):
        return (grid_index % 3 * self.grid_size[0], grid_index // 3 * self.grid_size[1])

    def find_adjacent_grids(self):
        adj_grids = []

        if self.empty_grid_index % 3 != 0:
            adj_grids.append(self.empty_grid_index - 1)
        if self.empty_grid_index % 3 != 2:
            adj_grids.append(self.empty_grid_index + 1)
        if self.empty_grid_index // 3 != 0:
            adj_grids.append(self.empty_grid_index - 3)
        if self.empty_grid_index // 3 != 2:
            adj_grids.append(self.empty_grid_index + 3)

        return adj_grids

    def swap_grids(self,grid1_index, grid2_index):
        
        if grid1_index == self.empty_grid_index:
            self.empty_grid_index = grid2_index
        elif grid2_index == self.empty_grid_index:
            self.empty_grid_index = grid1_index

        self.grids[grid1_index], self.grids[grid2_index] = self.grids[grid2_index], self.grids[grid1_index]
        self.state[grid1_index], self.state[grid2_index] = self.state[grid2_index], self.state[grid1_index]
        
        self.update_display()

    def on_grid_click(self,event):
        clicked_grid_index = event.widget.grid_index
        adjacent_grids = self.find_adjacent_grids()
        if clicked_grid_index in adjacent_grids:
            self.swap_grids(clicked_grid_index, self.empty_grid_index)

    def print_hello(self):
        # global AI_Toggle
        self.AI_Toggle=self.AI_Toggle^1
        # print('clicked')

    def update_display(self):
        # global AI_Toggle
        for i in range(9):
            x, y = self.get_grid_position(i)
            grid_image = ImageTk.PhotoImage(self.grids[i])
            self.labels[i].configure(image=grid_image)
            self.labels[i].image = grid_image
        if self.AI_Toggle:
            state_x = self.state.reshape((3, 3))
            actions = self.x_model(state_x)
            if len(actions)>1:
                self.AI_Toggle=0
            action_list=''
            for action in actions:
                 action_list+=move[action]
            self.action_textbox.delete('1.0', tk.END)  # Clear previous text
            self.action_textbox.insert(tk.END, action_list)
            # print('\n', state_x)
    def render_game(self,model,image):
        root = tk.Tk()
        # root= tk.Toplevel()
        if not image:
            image="terminator.png"
        
        image = Image.open(image) 
        root.title('Prove you are a HUMAN')
        self.grid_size = (image.width // 3, image.height // 3)


        state, pos = generate_random_state()
        self.state=state.flatten()
        state_1 = self.state.reshape(3,3)
        # print(state_1)
        self.x_model=model
        actions = self.x_model(state_1)
        self.AI_Toggle=0 
        action_list=''     
        for action in actions:
            action_list+=move[action]
        # print('\n')
        # print(state)
        empty_grid_index = self.state.tolist().index(8)
        grid_new = [image.crop(self.get_grid_position(i) + (self.get_grid_position(i)[0] + self.grid_size[0], self.get_grid_position(i)[1] + self.grid_size[1])) for i in self.state]

        grids = []
        self.labels = []
        for i in range(9):
            if i != empty_grid_index:
                grids.append(grid_new[i])
            else:
                grids.append(Image.new('RGB', self.grid_size, color='black'))
        self.grids=grids
        self.empty_grid_index=empty_grid_index
        for i in range(9):
            x, y = self.get_grid_position(i)
            grid_image = ImageTk.PhotoImage(grids[i])
            label = tk.Label(root, image=grid_image)
            
            label.grid(row=i // 3, column=i % 3)
            label.grid_index = i
            label.image = grid_image
            self.labels.append(label)
            label.bind("<Button-1>", self.on_grid_click)

       
        hello_button = tk.Button(root, text="Let AI Help", command=self.print_hello)
        hello_button.grid(row=3, columnspan=3)
        self.action_textbox = tk.Text(root, height=2, width=50)
        self.action_textbox.grid(row=4, columnspan=3)
        self.action_textbox.insert(tk.END, action_list)
        root.mainloop()

