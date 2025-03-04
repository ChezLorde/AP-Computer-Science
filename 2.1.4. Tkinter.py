#   A program creates a window on your screen using Tkinter.
import tkinter as tk
import tkinter.scrolledtext as tksc

# Login button function
def login():
  frame_auth.tkraise()

# main window
root = tk.Tk()
root.wm_geometry("150x200")
root.wm_title("Authorization")

# Login Frame
frame_login = tk.Frame(root)
frame_login.grid(row=0, column=0, sticky="news")

# Authorization Frame
frame_auth = tk.Frame(root)
frame_auth.grid(row=0, column=0, sticky="news")

# Auth Text
lbl_banana = tk.Label(frame_auth, text="Banana")
lbl_banana.pack(padx=0)
lbl_banana["font"] = "Courier"

# Username label
lbl_username = tk.Label(frame_login, text="Username: ")
lbl_username.pack(pady=0)
lbl_username["font"] = "Courier"

# Username entry
ent_username = tk.Entry(frame_login, bd=3)
ent_username.pack(pady=5)

# Password label
lbl_password = tk.Label(frame_login, text="Password: ")
lbl_password.pack(padx=0)
lbl_password["font"] = "Courier"

# Password entry
ent_password = tk.Entry(frame_login, bd=3, show="*")
ent_password.pack(pady=5)

# Login button
bt_image = tk.PhotoImage(file="login_button.gif")
bt_image = bt_image.subsample(10,10)
login_button = tk.Button(frame_login, text="Login", command=login, image=bt_image)
login_button.pack(padx=50)

frame_login.tkraise()

test_textbox = tksc.ScrolledText(frame_auth)
test_textbox.configure(height=10, width=50)
test_textbox.pack(padx=0)

root.mainloop()