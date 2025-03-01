import tkinter as tk
from tkinter import PhotoImage
from tkinter import Canvas
from tkinter import *
from tkinter import Toplevel, Label,Button
from PIL import ImageTk,Image
from datetime import *
import calendar
import subprocess
import atexit
import cv2
import depthai as dai
import numpy as np
#import blobconverter
import sys
import warnings
import threading
from difflib import get_close_matches
import os

root = tk.Tk()
root.title('monkfish')
root.geometry("720x720")

wf_var = tk.StringVar()
wt_var = tk.StringVar()

#command = ["/snap/bin/ngrok", "http", "--url=fancy-active-monkfish.ngrok-free.app", "80"]
#process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#print("ngrok started.")
#with open("/home/pi/main/Chat/app.py") as file:
    #exec(file.read())
#print("ws started")

coins = 0
no_close = None

import tkinter as tk
from PIL import Image, ImageTk

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

import tkinter as tk
from PIL import Image, ImageTk

my_locations = ["Mrs Newbury's Office", 'Bowie', 'Staff Office', 'Girls Bathroom 1', 'Boys Bathroom 1', 'Chaplin', 'Back Door Exit', 'Front Door Exit', 'Kitchen', 'Indira', 'Einstein', 'Dussoix', 'Berners-Lee', 'Girls Bathroom 2', 'Boys Bathroom 2', 'Chevrolet', 'Gosteli', 'Library', 'Kollontai', 'Girls Bathroom c_corridor', 'Boys Bathroom c_corridor', 'Ms Hutcheson', 'Mr Crabtree', 'Boys Bathroom d_corridor', 'Girls Bathroom d_corridor', 'De Sassure', 'Klee', 'Dunant', 'Maillart', 'Capela']

def set_default_():
        with open("/home/pi/main/save_data.txt", 'w') as file:
            file.write(str("[]"))

def display_image(image_path):
    try:
        # Use a default image if image_path is None
        if image_path is None:
            image_path = "/home/pi/main/default.png"  # Default image
            
        # Check if the file exists
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return
            
        img = Image.open(image_path)
        img = img.resize((50, 50), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label = Label(root, image=photo, borderwidth=2, relief="solid")
        label.image = photo
        label.pack(side="top", anchor="e")
    except Exception as e:
        print(f"Error displaying image: {e}")


def find_closest(word, word_list):
   matches = get_close_matches(word, word_list, n=1, cutoff=0.3)
   return matches[0] if matches else "No close match found"

def main_code():
    global coins,pth, locations
    
    import warnings
    import numpy as np
    import matplotlib.pyplot as plt, matplotlib.patheffects as pe
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder

    coins += 1

    warnings.filterwarnings("ignore")
    
    locations = {
        "Mrs Newbury's Office": [[1, 2], "main_floor"],
        "Bowie": [[9, 1], "main_floor"],
        "Staff Office": [[9, 6], "main_floor"],
        "Girls Bathroom 1": [[5, 6], "main_floor"],
        "Boys Bathroom 1": [[5, 7], "main_floor"],
        "Chaplin": [[2, 6], "main_floor"],
        "Back Door Exit": [[8, 13], "main_floor"],
        "Front Door Exit": [[42, 14], "main_floor"],
        "Kitchen": [[44, 30], "main_floor"],
        "Indira": [[56, 18], "main_floor"],
        "Einstein": [[52, 23], "main_floor"],
        "Dussoix": [[81, 23], "main_floor"],
        "Berners-Lee": [[83, 18], "main_floor"],
        "Girls Bathroom 2": [[49, 18], "main_floor"],
        "Boys Bathroom 2": [[49, 23], "main_floor"],
        "Chevrolet": [[7, 1], "d_corridor"],
        "Gosteli": [[14, 6], "d_corridor"],
        "Library": [[20, 6], "d_corridor"],
        "Kollontai": [[34, 1], "d_corridor"],
        "Girls Bathroom c_corridor": [[29, 6], "d_corridor"],
        "Boys Bathroom c_corridor": [[29, 1], "d_corridor"],
        "Ms Hutcheson": [[4, 2], "c_corridor"],
        "Mr Crabtree": [[1, 24], "c_corridor"],
        "Boys Bathroom d_corridor": [[11, 21], "c_corridor"],
        "Girls Bathroom d_corridor": [[11, 27], "c_corridor"],
        "De Sassure": [[20, 21], "c_corridor"],
        "Klee": [[20, 27], "c_corridor"],
        "Dunant": [[28, 21], "c_corridor"],
        "Maillart": [[28, 27], "c_corridor"],
        "Capela": [[34, 21], "c_corridor"]
    }
    

    def pathfind(s, e):
        global grid_data, grid
        finder = AStarFinder()

        grid_data = np.genfromtxt(f'/home/pi/main/{eval(s)[1]}.txt', dtype=int)
        grid = Grid(matrix=grid_data)

        for y in range(grid_data.shape[0]):
            for x in range(grid_data.shape[1]):
                grid.nodes[y][x].walkable = (grid_data[y][x] == 0)

        s_list = [eval(s)[0], grid.node(eval(s)[0][0], eval(s)[0][1])]

        if eval(s)[1] == eval(e)[1]:
            stairs = 0
        elif eval(s)[1] in ("c_corridor", "d_corridor", "stairway") and eval(e)[1] in ("c_corridor", "d_corridor", "stairway"):
            stairs = "same floor"
        elif eval(s)[1] in ("c_corridor", "d_corridor", "stairway") and eval(e)[1] == "main_floor":
            stairs = "down"
            
        elif eval(e)[1] in ("c_corridor", "d_corridor", "stairway") and eval(s)[1] == "main_floor":
            stairs = "up"
        else:
            stairs = "error"

        print(stairs)

        if stairs == 0:
            e_list = [eval(e)[0], grid.node(eval(e)[0][0], eval(e)[0][1])]
            start = [s_list[0], s_list[1]]
            end = [e_list[0], e_list[1]]

        if stairs == "same floor":
            start = [s_list[0], s_list[1]]
            if eval(s)[1] == "d_corridor":
                end = [[50, 19], grid.node(50, 19)]
            elif eval(s)[1] == "stairway" and eval(e)[1] == "c_corridor":
                end = [[5, 5], grid.node(5, 5)]
            elif eval(s)[1] == "stairway" and eval(e)[1] == "d_corridor":
                end = [[0, 5], grid.node(0, 5)]
            elif eval(s)[1] == "c_corridor":
                end = [[3, 0], grid.node(3, 0)]

        if stairs == "down":
            start = [s_list[0], s_list[1]]
            if eval(s)[1] == "d_corridor":
                end = [[50, 19], grid.node(50, 19)]
            elif eval(s)[1] == "c_corridor":
                end = [[3, 0], grid.node(3, 0)]
            elif eval(s)[1] == "stairway":
                end = [[16, 10], grid.node(16, 10)]

        if stairs == "up":
            start = [s_list[0], s_list[1]]
            end = [[39, 15], grid.node(39, 15)]

        if stairs == "error":
            print("Error in pathfinding")

        path, runs = finder.find_path(start[1], end[1], grid)
        return path, start, end, stairs

    def qr_scan():
        try:
            with open("/home/pi/main/main_qr.py", "r") as file:
                try:
                    exec(file.read())
                    sc_l.destroy()
                except SystemExit:
                    pass
            return data
        except Exception as e:
            print(f"Error in QR scan: {e}")
            return None

    def main_navigation_loop():
        print("Waiting for QR code data...")
        start_input = qr_scan()

        if start_input:
            print(f"Start coordinate received: {start_input}")
            try:
                pass
            except:
                pass
                sys.stdin = open('/dev/tty', 'r')

            if input_ not in ("Boys Bathroom", "Girls Bathroom"):
                print(input_)
                end_input = str(locations[input_])
                if eval(start_input) == end_input:
                    print("You have arrived at your destination.")
                    return
            else:
                if eval(start_input)[1] == "main_floor":
                    path1, start, end, stairs = pathfind(start_input, str(locations[f"{input_} 1"]))
                    path2, start, end, stairs = pathfind(start_input, str(locations[f"{input_} 2"]))
                    closest_bathroom = f"{input_} 2" if len(path1) >= len(path2) else f"{input_} 1"
                    end_input = locations[closest_bathroom]
                    if eval(start_input) == end_input:
                        print("You have arrived at your destination.")
                        return
                else:
                    end_input = locations[f"{input_.strip()} {eval(start_input)[1]}"]
                    if eval(start_input) == end_input:
                        print("You have arrived at your destination.")
                        return

            try:
                path, start, end, stairs = pathfind(start_input, end_input)
            except:
                path, start, end, stairs = pathfind(start_input, str(end_input))

            print(start, end)

            grid_viz = grid_data.astype(float)
            path_coords = [(node.x, node.y) for node in path]
            data = waypoints(path_coords)
            print(data)
            instructions = get_instructions(path_coords)
            for x, y in path_coords:
                grid_viz[y][x] = 2
            grid_viz[start[0][1]][start[0][0]] = 3
            grid_viz[end[0][1]][end[0][0]] = 4
            import matplotlib.pyplot as plt
            plt.figure(figsize=(12, 8))
            try:
                for name, (x, y) in data:
                    plt.scatter(x, y, label=name)
                    plt.text(x, y, name, fontsize=7, ha='right', color='white').set_path_effects([pe.withStroke(linewidth=3, foreground='black')]) # LABELS ADDED HERE
            except:
                pass
            plt.imshow(grid_viz, cmap='viridis')
            plt.axis('off')
            plt.title('Pathfinding Grid')
            plt.savefig('/home/pi/main/pathfinding_grid.png', bbox_inches='tight', pad_inches=0)
            plt.close()
            clear()
            with open("/home/pi/main/save_data.txt", 'r') as file:
                content = file.read().strip()
                if content:
                    try:
                        save_data = eval(content)[0]
                    except:
                        save_data = None
                else:
                    save_data = None
            display_image(save_data)
            global p1, p2
            current_loc = eval(start_input)[1]
            if current_loc[0] == "d":
                current_loc = "in the D corridor"
            elif current_loc[0] == "c":
                current_loc = "in the C corridor"
            elif current_loc[0] == "m":
                current_loc = "on the Main Floor"
            elif current_loc[0] == "s":
                current_loc = "in the stairway"
            main_frame = tk.Frame(root)
            main_frame.pack(side="top", fill="both", expand=True)
            map_frame = tk.Frame(main_frame)
            map_frame.pack(side="top", fill="both")
            bottom_frame = tk.Frame(main_frame)
            bottom_frame.pack(side="bottom", fill="both", expand=True)
            button_frame = tk.Frame(bottom_frame)
            button_frame.pack(side="left", fill="y", padx=10, pady=10)
            directions_frame = tk.Frame(bottom_frame)
            directions_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
            label = tk.Label(button_frame, text='You are ' + current_loc + ' and the\n destination is ' + closest, compound='top', font=("Lexend", 10))
            label.pack(pady=10)
            img = Image.open('/home/pi/main/pathfinding_grid.png')
            p1 = ImageTk.PhotoImage(img.resize((620, 400), Image.Resampling.LANCZOS))
            tk.Label(map_frame, image=p1).pack()
            tk.Button(button_frame, text="Scan again to update map", bg="sky blue", fg="white", command=main_code, font=("Lexend", 10)).pack(pady=5)
            tk.Button(button_frame, text="Stop Navigating", bg="red", fg="white", command=lambda:[clear(), start_screen()], font=("Lexend", 10)).pack(pady=5, padx=5)
            if stairs in ["down", "up"]:
                img_path = '/home/pi/main/down_stairs.png' if stairs == "down" else '/home/pi/main/up_stairs.png'
                p2 = ImageTk.PhotoImage(Image.open(img_path).resize((125, 125), Image.Resampling.LANCZOS))
                l = tk.Label(button_frame, image=p2)
                l.pack(pady=5)
                b = tk.Button(button_frame, text="OK", bg="sky blue", fg="white", command=lambda:[l.destroy(), b.destroy()], font=("Lexend", 15))
                b.pack(pady=5)
            scrollbar = tk.Scrollbar(directions_frame)
            scrollbar.pack(side="right", fill="y")
            lb = tk.Listbox(directions_frame, font=("Lexend", 20), yscrollcommand=scrollbar.set)
            for inst in instructions:
                lb.insert(tk.END, inst)
            lb.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=lb.yview)
            root.mainloop()



    main_navigation_loop()


def get_delta(p1, p2):
    return (p2[0] - p1[0], p2[1] - p1[1])

def get_turn_instruction(current_delta, next_delta):
    cross = current_delta[0] * next_delta[1] - current_delta[1] * next_delta[0]
    dot = current_delta[0] * next_delta[0] + current_delta[1] * next_delta[1]
    if cross > 0:
        return "Turn right"
    elif cross < 0:
        return "Turn left"
    elif dot < 0:
        return "Turn around"
    else:
        return "Continue straight"

def get_instructions(path):
    if len(path) < 2:
        return []
    instructions = []
    current_delta = get_delta(path[0], path[1])
    step_count = 1
    for i in range(1, len(path) - 1):
        next_delta = get_delta(path[i], path[i + 1])
        if next_delta == current_delta:
            step_count += 1
        else:
            instructions.append(f"Go forward {step_count} step{'s' if step_count != 1 else ''}")
            instructions.append(get_turn_instruction(current_delta, next_delta))
            current_delta = next_delta
            step_count = 1
    instructions.append(f"Go forward {step_count} step{'s' if step_count != 1 else ''}")
    return instructions

def directions(pth):
    listtt = []
    try:
        for inst in get_instructions(pth):
            listtt.append(inst)
        print(listtt)
    except Exception as e:
        print(f"Error in directions: {e}")



def waypoints(pth):
    path_coords = pth

    path_set = set(path_coords)
    
    listt = []
    

    locations_main_on_path = {
        name: coord for name, (coord, floor) in locations.items()
        if floor == "main_floor" and tuple(coord) in path_set
    }
    

    if locations_main_on_path:
        print("The following main floor locations are on the path:")
        for name, coord in locations_main_on_path.items():
            listt.append([name,coord])
        return listt
    else:
        print("No main floor locations are on the path.")

def qr_scan():
   try:
       with open("/home/pi/main/main_qr.py", "r") as file:
           try:
               exec(file.read())
           except SystemExit:
               pass
       return data 
   except Exception as e:
       print(f"Error in QR scan: {e}")
       return None

# Utility functions
def hide_button(widget):
    widget.pack_forget()

def show_button(widget):
    widget.pack()

def ready_next_page():
    clear()

def submit_nav(sub="nav"):
    global input_, no_close, closest
    clear()
    print(f"To: {wt_var.get()}" if sub == "nav" else f"To: {sub}")
    wf = tk.Label(root, text="Where From?", font=("Lexend", 20))
    wf.pack(pady=10)
    image = Image.open("/home/pi/main/Nearest_QR.png")
    resized_image = image.resize((200, 200))
    image_qr_prompt = ImageTk.PhotoImage(resized_image)
    label = tk.Label(root, text='QR codes can be found in \n hallways stuck to the walls. \n Simply hold up your device the \n the paper and it scans automatically.\n To update your map, use the scanner\n to scan the closest QR code', image=image_qr_prompt, compound='top')
    label.pack(side="top", anchor="center", padx=50, pady=50)
    label.image = image_qr_prompt
    test_word = wt_var.get()
    closest = find_closest(test_word, my_locations)
    if closest == "No close match found":
        no_close = True
        start_nav()
    else:
        no_close = False
        print(f"Input: {test_word}")
        print(closest)
        input_ = closest
        root.after(100, main_code)

def back():
    clear()
    start_screen()

def where_from():
    global wf, wf_entry, sub_btn,input_
    strt_btn.destroy()
    pr.destroy()
    wf = tk.Label(root, text="Where From?", font=("Lexend", 20))
    wf.pack(pady=10)
    image = Image.open("/home/pi/main/Nearest_QR.png")
    resized_image = image.resize((200, 200))
    image_qr_prompt = ImageTk.PhotoImage(resized_image)
    label = tk.Label(root, text='QR codes can be found in \n hallways stuck to the walls. \n Simply hold up your device the \n the paper and it scans automatically.\n To update your map, use the scanner\n to scan the closest QR code', image=image_qr_prompt, compound='top')
    label.pack(side="top", anchor="center", padx=50, pady=50)
    label.image = image_qr_prompt
    input_ = day_data[i]['dest']
    root.after(100, main_code)
    

def see_nxt_ls():
    global pred, day_data, i
    def describe(a):
        snake = []
        for i in range(len(a)):
            b = a[i].split(",")
            ekans = b[0].split(":")
            ekans1 = b[1].split(":")
            c = {
                'start': time(int(ekans[0]), int(ekans[1])),
                'end': time(int(ekans1[0]), int(ekans1[1])),
                'subj': b[2],
                'prof': b[3],
                'dest': b[4]
            }
            snake.append(c)
        return snake

    def dictionary(txt):
        with open(txt, "r") as f:
            content = f.readlines()

        results = {}
        for line in content:
            x = line.strip().split("@")
            if len(x) >= 2:
                results[x[0]] = x[-1]

        answer = {
            'Monday': describe(results.get('Monday', "").split("$")),
            'Tuesday': describe(results.get('Tuesday', "").split("$")),
            'Wednesday': describe(results.get('Wednesday', "").split("$")),
            'Thursday': describe(results.get('Thursday', "").split("$")),
            'Friday': describe(results.get('Friday', "").split("$"))
        }
        return answer

    data = dictionary("/home/pi/main/txtfil3.txt")
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]

    if day in ["Saturday", "Sunday"]:
        print("Weekend!!!!")
        pred_text = "NO"
        return

    day_data = data.get(day, [])
    if not day_data:
        print(f"No schedule available for {day}")
        pred_text = "NO"
        return

    now = datetime.now().time()

    for i in range(len(day_data)):
        if day_data[i]['start'] >= now:
            if i == 0 or day_data[i - 1]['end'] >= now:
                print(day_data[i])
                print(f"Your next class starts at {day_data[i]['start']} with {day_data[i]['prof']} in {day_data[i]['dest']}. The subject is {day_data[i]['subj']}.")
                listret = []
                # Create and pack the label for the prediction
                pred_text = f"Your next class starts \n at {day_data[i]['start']} \n with {day_data[i]['prof']} \n in {day_data[i]['dest']}.  \n The subject is \n {day_data[i]['subj']}."
                pred = tk.Label(root, text=pred_text, font=("Lexend", 20))
                listret.append(pred_text)
                listret.append(day_data[i])
                return listret

    print("No more classes today.")
    pred_text = "NO"

def start_achi():
    clear()
    
    if coins == 0:
        _file_ = "/home/pi/main/lock.png"
        txxt = "Locked"
    else:
        _file_ = "/home/pi/main/1st_scan.png"
        txxt = "Congrats! You scanned for the first time!"

    image_lock = Image.open(_file_)
    image_lock = image_lock.resize((55, 55))
    image_lock = ImageTk.PhotoImage(image_lock)
    label = tk.Label(root, text=txxt, image=image_lock, compound='top')
    label.pack(side="top", anchor="center", padx=50, pady=15)
    label.image = image_lock
    
    if timet == False:
        _file_ = "/home/pi/main/lock.png"
        txxt = "Locked"
    else:
        _file_ = "/home/pi/main/1st_timetable.png"
        txxt = "Congratulations! You read the timetable for the first time!"
        
    image_lock = Image.open(_file_)
    image_lock = image_lock.resize((55, 55))
    image_lock = ImageTk.PhotoImage(image_lock)
    label = tk.Label(root, text=txxt, image=image_lock, compound='top')
    label.pack(side="top", anchor="center", padx=50, pady=15)
    label.image = image_lock

    if coins < 10:
        _file_ = "/home/pi/main/lock.png"
        txxt = "Locked"
    else:
        _file_ = "/home/pi/main/10th_scan.png"
        txxt = "Well Done! You scanned 10 qr codes!"

    image_lock = Image.open(_file_)
    image_lock = image_lock.resize((55, 55))
    image_lock = ImageTk.PhotoImage(image_lock)
    label = tk.Label(root, text=txxt, image=image_lock, compound='top')
    label.pack(side="top", anchor="center", padx=50, pady=15)
    label.image = image_lock

    if bt_crwn == False:
        _file_ = "/home/pi/main/lock.png"
        txxt = "Locked"
    else:
        _file_ = "/home/pi/main/bought_crwn.png"
        txxt = "Well Done! You bought the most expensive item in the shop!"

    image_lock = Image.open(_file_)
    image_lock = image_lock.resize((55, 55))
    image_lock = ImageTk.PhotoImage(image_lock)
    label = tk.Label(root, text=txxt, image=image_lock, compound='top')
    label.pack(side="top", anchor="center", padx=50, pady=15)
    label.image = image_lock
    
    back__btn = tk.Button(root, text="Back", bg="sky blue", fg="white", command=back, font=("Lexend", 10))  # Corrected command here
    back__btn.pack(side="top", anchor="center", padx=50, pady=50)


	
def start_nav():
    clear()
    ready_next_page()
    
    global wt, sub_btn, wt_entry, bck_btn
    
    if no_close == True:
            clear()
            wt = tk.Label(root, text="Input could not be recognised",fg = "red", font=("Lexend", 20))
            wt.pack(pady=10)

    wt = tk.Label(root, text="Where To?", font=("Lexend", 20))
    wt.pack(pady=10)

    wt_entry = tk.Entry(root, textvariable=wt_var, font=('Lexend', 20, 'bold'))
    wt_entry.pack(pady=10)

    sub_btn = tk.Button(root, text='Start',bg="sky blue", fg="white", command=lambda: submit_nav("nav"), font=('Lexend', 20, 'bold'))
    sub_btn.pack(pady=20)

    bck_btn = tk.Button(root, text='Back',bg="sky blue", fg="white", command=back, font=('Lexend', 20, 'bold'))
    bck_btn.pack(pady=20)

def start_timetable():
    global strt_btn, back__btn, lesson_place,pr
    ready_next_page()
    prediction = see_nxt_ls()
    if prediction == None:
        nosa = tk.Label(root, text='Timetable prediction \n not available.', font=("Lexend", 20))
        nosa.pack(pady=40)
        back__btn = tk.Button(root, text="Back", bg="sky blue", fg="white", command=back, font=("Lexend", 25))  # Corrected command here
        back__btn.pack(pady=40)

    else:
        pr = tk.Label(root, text=prediction[0], font=("Lexend", 20))
        pr.pack(pady=10)
        lesson_place = prediction[1]['dest']
        strt_btn = tk.Button(root, text="Start!", bg="sky blue", fg="white", command=lambda:[where_from(),timet == True], font=("Lexend", 25))
        strt_btn.pack(pady=10)
        back__btn = tk.Button(root, text="Back", bg="sky blue", fg="white", command=back, font=("Lexend", 25))  # Corrected command here
        back__btn.pack(pady=40)

def clear():
    for widget in root.winfo_children():
        widget.pack_forget() 

def start_mssg():
	clear()
	back__btn = tk.Button(root, text="Back", bg="sky blue", fg="white", command=back, font=("Lexend", 25))  # Corrected command here
	back__btn.pack(pady=40)


def exit_handler():
	print("\nStopping ngrok...")
	process.terminate()

def buy_item(which):
    global coins

    item_costs = {
        "/home/pi/main/icecream.png": 10,
        "/home/pi/main/radio.png": 20,
        "/home/pi/main/trumpet.png": 50,
        "/home/pi/main/drink.png": 60,
        "/home/pi/main/crown.png": 60
    }

    # Check if the user has enough coins
    if coins < item_costs[which]:
        messagebox.showwarning("Not enough coins", f"You need {item_costs[which]} coins to buy this item!")
        return

    # Deduct coins for the purchase
    coins -= item_costs[which]

    # Try reading the existing save data
    try:
        with open("/home/pi/main/save_data.txt", 'r') as file:
            current_data = file.read().strip()
    except FileNotFoundError:
        current_data = ""

    # Show success message with updated coin balance
    messagebox.showinfo("Success", f"Item purchased successfully!\nYou have {coins} coins remaining.")

    with open("/home/pi/main/save_data.txt", 'w') as file:
        file.write(f'["{which}"]')

    # Refresh the shop interface
    start_shop()


def start_shop():
    global coins
    
    clear()
    
    money = tk.Label(root, text=f'Coins: {coins}', font=("Lexend", 20))
    money.pack(pady=5)
    
    image_itm1 = PhotoImage(file="/home/pi/main/icecream.png")
    label1 = tk.Label(root, image=image_itm1, compound='top')
    label1.pack(side="top", anchor="w", padx=50, pady=5)
    label1.image = image_itm1  

    button_buy_itm1 = tk.Button(root, text="10 coins", bg="sky blue", fg="white", command=lambda: buy_item("/home/pi/main/icecream.png"), font=("Lexend", 10))
    button_buy_itm1.pack(anchor="w", padx=30, pady=5)

    # Item 2: Radio
    image_itm2 = PhotoImage(file="/home/pi/main/radio.png")
    label2 = tk.Label(root, image=image_itm2, compound='top')
    label2.pack(side="top", anchor="w", padx=25, pady=5)
    label2.image = image_itm2  

    button_buy_itm2 = tk.Button(root, text="20 coins", bg="sky blue", fg="white", command=lambda: buy_item("/home/pi/main/radio.png"), font=("Lexend", 10))
    button_buy_itm2.pack(anchor="w", padx=30, pady=5)

    # Item 3: Trumpet
    image_itm3 = PhotoImage(file="/home/pi/main/trumpet.png")
    label3 = tk.Label(root, image=image_itm3, compound='top')
    label3.pack(side="top", anchor="w", padx=30, pady=5)
    label3.image = image_itm3

    button_buy_itm3 = tk.Button(root, text="50 coins", bg="sky blue", fg="white", command=lambda: buy_item("/home/pi/main/trumpet.png"), font=("Lexend", 10))
    button_buy_itm3.pack(anchor="w", padx=30, pady=15)
    
    button_next_page = tk.Button(root, text="Next Page", bg="sky blue", fg="white", command=shp_nxtpg, font=("Lexend", 20)) 
    button_next_page.pack(anchor="center", padx=30, pady=5)
    
    #Back
    back__btn = tk.Button(root, text="Back", bg="sky blue", fg="white", command=back, font=("Lexend", 20)) 
    back__btn.pack(pady=0)

def shp_nxtpg():
    
    clear()
    # Item 4: Trumpet
    image_itm4 = PhotoImage(file="/home/pi/main/drink.png")
    label4 = tk.Label(root, image=image_itm4, compound='top')
    label4.pack(side="top", anchor="w", padx=30, pady=15)
    label4.image = image_itm4
    
    button_buy_itm4 = tk.Button(root, text="60 coins", bg="sky blue", fg="white", command=lambda: buy_item("/home/pi/main/drink.png"), font=("Lexend", 10))
    button_buy_itm4.pack(anchor="w", padx=30, pady=5)
    
    # Item 5: Crown
    image_itm5 = PhotoImage(file="/home/pi/main/crown.png")
    label5 = tk.Label(root, image=image_itm5, compound='top')
    label5.pack(side="top", anchor="w", padx=30, pady=15)
    label5.image = image_itm5

    button_buy_itm5 = tk.Button(root, text="60 coins", bg="sky blue", fg="white", command=lambda: [buy_item("/home/pi/main/crown.png"),bt_crwn == True], font=("Lexend", 10))
    button_buy_itm5.pack(anchor="w", padx=30, pady=5)
    
    dflt_st = tk.Button(root, text="Set item back to default\n - This will mean you will have to buy back your picture to equip it -", bg="sky blue", fg="white", command=lambda: [set_default_(), print("d")], font=("Lexend", 10))
    dflt_st.pack(anchor="w", padx=30, pady=30)

    
    #Back
    back__btn = tk.Button(root, text="Previous page", bg="sky blue", fg="white", command=start_shop, font=("Lexend", 20)) 
    back__btn.pack(pady=35)
    
    
def show_feed():
    try:
        with open("/home/pi/main/friend_finder.py", "r") as file:
            try:
                exec(file.read())
                sc_l.destroy()
            except SystemExit:
                pass
        return data
    except Exception as e:
        print(f"Error in QR scan: {e}")
        return None
    
def friendfinder():
    clear()
    back__btn = tk.Button(root, text="Back", bg="sky blue", fg="white", command=back, font=("Lexend", 20)) 
    back__btn.pack(pady=0)
    
    root.after(100, show_feed)
    
    



def start_screen():
    global image_refs  # Store image references to prevent garbage collection

    # Define icon size
    icon_size = (150, 150)

    # Base path for images
    base_path = "C:\\Users\\mubas\\Downloads\\gui test 2\\"

    # Dictionary with button labels, image file names, and their corresponding functions
    button_data = [
        ("Navigation", base_path + "navigation.png", start_nav),
        ("Timetable", base_path + "timetable.png", start_timetable),
        ("Achievements", base_path + "rewards.png", start_achi),
        ("Messaging", base_path + "message.png", start_mssg),
        ("Shop", base_path + "shop.png", start_shop),
        ("Friends", base_path + "friend.png", friendfinder)
    ]

    # Store image references globally to prevent garbage collection
    image_refs = {}

    # Load images AFTER Tk() initializes
    for name, path, _ in button_data:
        img = Image.open(path).resize(icon_size)
        image_refs[name] = ImageTk.PhotoImage(img)  # Store reference

    # Create a frame for layout
    frame = tk.Frame(root, bg="#F5F5F7")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Function to create buttons with text labels underneath
    def create_button_with_label(name, command, row, col):
        img = image_refs[name]  # Retrieve stored image

        # Create a container frame for the button + label
        container = tk.Frame(frame, bg="#F5F5F7")
        container.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Image button
        btn = tk.Button(container, image=img, bg="#F5F5F7", activebackground="#E5E5EA",
                        relief="flat", bd=0, highlightthickness=0, command=command)
        btn.pack()

        # Text label under button
        label = tk.Label(container, text=name, font=("Lexend", 12), bg="#F5F5F7", fg="#000000")
        label.pack()

    # Create buttons in a 2x3 grid
    for i, (name, _, command) in enumerate(button_data):
        create_button_with_label(name, command, i // 2, i % 2)

    # Configure grid to make layout dynamic
    for i in range(3):  # 3 rows
        frame.rowconfigure(i, weight=1)
    for j in range(2):  # 2 columns
        frame.columnconfigure(j, weight=1)

# Example command functions
#atexit.register(exit_handler)

start_screen()

root.mainloop()
