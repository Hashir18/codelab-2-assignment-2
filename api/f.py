import tkinter as tk
from tkinter import Entry, Label, Button, Listbox, END, Toplevel, LEFT, RIGHT
import requests
import io
from PIL import Image, ImageTk


def data_fetch(api_key, query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': api_key,
        'query': query
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data['results']

def fetch_details(api_key, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        'api_key': api_key,
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data

def movie_result(movies):
    listbox.delete(0, END)

    for movie in movies:
        Movie_name = movie.get('title', 'N/A') 
        listbox.insert(tk.END, Movie_name)

def when_search():
    global movies
    query = entry.get()
    if query:
        movies = data_fetch(api_key, query)
        movie_result(movies)

def movie_selection(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_movie = movies[selected_index[0]]
        movie_details(selected_movie['id'])

def movie_details(movie_id):
    movie_details = fetch_details(api_key, movie_id)

    if movie_details:
        Movie_name = movie_details.get("title", "N/A") 
        details = movie_details.get("overview", "N/A") 
        movie_release = movie_details.get("release_date", "N/A") 
        img = movie_details.get("poster_path", "")

        details2 = details[:300] + "..." if len(details) > 300 else details

        details_lines = [details2[i:i + 100] for i in range(0, len(details2), 100)]

        full_description = f"Movie_name: {Movie_name}\nRelease Date: {movie_release}\n\ndetails:\n"
        full_description += "\n".join(details_lines)

        img_link = f"https://image.tmdb.org/t/p/original{img}"
        info_frame(full_description, img_link)

    else:
        full_description = f"No details found for this movie"
        info_frame(full_description, "")
  

def info_frame(full_description, img_link):
    info_fram = tk.Toplevel(root)
    info_fram.title("Movie Information")
    info_fram.geometry("600x400")  # Adjusted the size
    info_fram.configure(bg='black')  # Set background color

    if img_link:
        try:
            image_data = requests.get(img_link).content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((200, 300))
            photo = ImageTk.PhotoImage(image)
            img_label = tk.Label(info_fram, image=photo, bg='black')
            img_label.image = photo
            img_label.pack(side=tk.LEFT, padx=10, pady=10)  # Aligning image to the left

        except Exception as e:
            print(f"Error loading poster image: {e}")

    text_frame = tk.Frame(info_fram, bg='black')
    text_frame.pack(side=tk.RIGHT, padx=10, pady=10)  # Aligning text to the right

    info_label = tk.Label(text_frame, text=full_description, justify=tk.LEFT, wraplength=350, fg='white', bg='black')
    info_label.pack()

    if img_link:
        try:
            image_data = requests.get(img_link).content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((200, 300), Image.ANTIALIAS)  # Resizing the image
            photo = ImageTk.PhotoImage(image)
            img_label = Label(info_fram, image=photo)
            img_label.image = photo
            img_label.pack(side=LEFT, padx=10, pady=10)  # Aligning image to the left

        except Exception as e:
            print(f"Error loading poster image: {e}")

    info_label = Label(info_fram, text=full_description, justify=tk.LEFT)
    info_label.pack(side=RIGHT, padx=10, pady=10)  # Aligning text to the right

api_key = '709c3dbb893bd210ec18d9c731a1c7a6'

def show_frame(intropage):
    intropage.place(relwidth=1, relheight=1)


def switch_to_frame2():
    show_frame(frame2)

root = tk.Tk()
root.title("Frame Switcher App")
root.geometry("600x600")

frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

bg_image = tk.PhotoImage(file="bg.png")
bg_label = tk.Label(frame1, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

start_text = "Welcome to Aimon!\nDiscover information about your favorite movies."
start_label = tk.Label(frame1, text=start_text, font=("Helvetica", 16), fg="white", bg="black")
start_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)


action = tk.Button(frame1, text="Let's Start", bg="grey", fg="white", width=10, height=2, command=switch_to_frame2)
action.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#frame2
bgg_image = tk.PhotoImage(file="bg.png")
bgg_label = tk.Label(frame2, image=bgg_image)
bgg_label.place(relwidth=1, relheight=1)

entry_label = Label(frame2, text="Enter movie name:")
entry_label.pack(pady=10)
entry = Entry(frame2, width=30)
entry.pack(pady=10)

search_button = Button(frame2, text="Search", command=when_search)
search_button.pack(pady=10)

listbox = Listbox(frame2, width=40, height=10)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", movie_selection)

show_frame(frame1)

root.mainloop()
