import tkinter as tk
from tkinter import ttk
from langchain_back import get_few_shot_db_chain
def submit_question(question):
if question:
chain = get_few_shot_db_chain()
answer = chain.invoke(question)
answer_text.delete(1.0, tk.END) # Clear the text area
answer_text.insert(tk.END, answer) # Insert the answer
root = tk.Tk()
root.title(&quot;AtliQ T Shirts : Insights ��&quot;)
root.geometry(&quot;500x500&quot;)
# Create a frame to hold the question input
question_frame = ttk.Frame(root, padding=&quot;3 3 12 12&quot;)
question_frame.pack(pady=50)
# Create a label for the question prompt
question_label = ttk.Label(question_frame, text=&quot;Question:&quot;, font=(&quot;Arial&quot;, 14))
question_label.pack(side=tk.LEFT)
# Create the question input box
question_entry = ttk.Entry(question_frame, width=40)
question_entry.pack(side=tk.LEFT)
# Create a submit button
submit_button = ttk.Button(root, text=&quot;Submit&quot;, command=lambda:
submit_question(question_entry.get()))
submit_button.pack(pady=20)
# Create a text area for the answer
answer_text = tk.Text(root, height=10, width=50, wrap=tk.WORD, font=(&quot;Arial&quot;, 12))
answer_text.pack(pady=20)
root.mainloop()
