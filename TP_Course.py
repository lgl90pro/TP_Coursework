import locale
from datetime import datetime
from tkinter import *
from tkinter import messagebox, filedialog

all_history = str()
hst = 0
history = 0
error_count = 0
line_number = 0


# очищує поля для вводу і виводу
def clear_all():
    input_data.delete(0, END)
    output_data.delete(0, END)


# очищує історію переведень
def clear_history():
    global hst, all_history
    all_history = ''
    try:
        hst.destroy()
    except (TclError, AttributeError):
        pass


# показує вікно з помилкою введення, якщо така є
def errors(name):
    messagebox.showerror('Error', name)


# показує історію переведень в окремому вікні
def show():
    global hst, history, all_history

    try:
        hst.winfo_viewable()
    except (TclError, AttributeError):
        hst = Tk()
        hst.title('History')
        hst.iconbitmap('histoty.ico')
        hst.geometry('400x400+350+350')
        hst.resizable(False, False)
        history = Text(hst, padx=10, pady=10, font=('Arial', 11), bg='#2D1A3F', fg='#D3F011')

    history.delete(0.0, END)
    history.insert(END, all_history)
    history.place(x=0, y=0)
    hst.mainloop()


# зберігає історію переведень у зовнішній .txt файл
def save_to_file():
    global all_history

    fn = filedialog.SaveAs(root, filetypes=[('*.txt files', '.txt')]).show()
    if fn == '':
        return
    if not fn.endswith(".txt"):
        fn += ".txt"
    open(fn, 'wt').write(all_history)


# завантаження чисел із зовнішнього файлу
def load_from_file():
    global error_count, line_number

    fn = filedialog.Open(root, filetypes=[('*.txt files', '.txt')]).show()
    if fn == '':
        return
    file = open(fn, "r")
    lines = file.readlines()
    for line in lines:
        line_number += 1
        convert(line)
        if error_count != 0:
            error_count = 0
            line_number = 0
            break
    line_number = 0

    show()
    file.close


# переводить число із однієї системи числення в іншу
def convert(*digit):
    global all_history, error_count
    result = str()
    locale.setlocale(locale.LC_TIME, '')
    now = datetime.now()

    output_data.delete(0, END)
    if digit:
        num = ''.join(map(str, digit))
        num = num.replace('\n', '')
    else:
        num = input_data.get()
    num.strip()
    if len(num) == 0:
        errors('You must enter at least one number')
        error_count += 1
        return
    if input_check.get() == 0:
        errors('You must select a number system to enter')
        error_count += 1
        return
    if output_check.get() == 0:
        errors('You must select a number system to display')
        error_count += 1
        return

    # перевірка на число
    try:
        int(num, 16)
    except ValueError:
        if line_number == 0:
            errors('This is not a number!')
        else:
            errors(f'Characters in line {line_number} are not a number')
        error_count += 1
        return

    # перевірка на систему числення
    try:
        if input_check.get() == 2:
            num_copy = int(num, 2)
        elif input_check.get() == 8:
            num_copy = int(num, 8)
        elif input_check.get() == 10:
            num_copy = int(num)
        elif input_check.get() == 16:
            num_copy = int(num, 16)

        if output_check.get() == 2:
            result = bin(num_copy).replace('0b', '')
        elif output_check.get() == 8:
            result = oct(num_copy).replace('0o', '')
        elif output_check.get() == 10:
            result = num_copy
        elif output_check.get() == 16:
            result = hex(num_copy).replace('0x', '').upper()
    except ValueError:
        if line_number == 0:
            errors('The entered number does not match the selected number system.')
        else:
            errors(f'The entered number in line {line_number} does not match the selected number system.')
        error_count += 1
        return

    output_data.insert(0, result)
    all_history += f'{num}({str(input_check.get())})\t=====>\t{result}({str(output_check.get())})\n'
    all_history += now.strftime('%c\n')
    all_history += f'______________________________________________________________________\n\n'


# вікно програми
root = Tk()
root["bg"] = "#D3D3D3"
root.title('Numeral System Converter')
root.iconbitmap('icon.ico')
root.geometry('455x820+750+100')
root.resizable(False, False)

# фото у верхній частині програми
img = PhotoImage(file='icon3-1.png')
logo = Label(root, image=img)
logo.place(x=0, y=0)

# текст про вибір системи числення
text = Label(root, bg="#D3D3D3", fg='#8B0000', text='Choose a number system:', font=('Arial', 14))
text.place(y=325, relx=0.5, anchor='c')

# вибір із системи числення для вводу
input_check = IntVar()
input2 = Radiobutton(root, text='2', bg="#D3D3D3", activebackground='#D3D3D3', variable=input_check, value=2,
                     font=('Arial', 12, 'italic', 'bold'))
input8 = Radiobutton(root, text='8', bg="#D3D3D3", activebackground='#D3D3D3', variable=input_check, value=8,
                     font=('Arial', 12, 'italic', 'bold'))
input10 = Radiobutton(root, text='10', bg="#D3D3D3", activebackground='#D3D3D3', variable=input_check, value=10,
                      font=('Arial', 12, 'italic', 'bold'))
input16 = Radiobutton(root, text='16', bg="#D3D3D3", activebackground='#D3D3D3', variable=input_check, value=16,
                      font=('Arial', 12, 'italic', 'bold'))
input2.place(x=80, y=350)
input8.place(x=160, y=350)
input10.place(x=240, y=350)
input16.place(x=330, y=350)

# поле для введення
input_data = Entry(root, bd=5, font=('Comic Sans MS', 17, 'italic'), width=30, justify='c')
input_data.place(y=420, relx=0.5, anchor='c')

# вибір із системи числення для виведення
output_check = IntVar()
output2 = Radiobutton(root, text='2', bg="#D3D3D3", activebackground='#D3D3D3', variable=output_check, value=2,
                      font=('Arial', 12, 'italic', 'bold'))
output8 = Radiobutton(root, text='8', bg="#D3D3D3", activebackground='#D3D3D3', variable=output_check, value=8,
                      font=('Arial', 12, 'italic', 'bold'))
output10 = Radiobutton(root, text='10', bg="#D3D3D3", activebackground='#D3D3D3', variable=output_check, value=10,
                       font=('Arial', 12, 'italic', 'bold'))
output16 = Radiobutton(root, text='16', bg="#D3D3D3", activebackground='#D3D3D3', variable=output_check, value=16,
                       font=('Arial', 12, 'italic', 'bold'))
output2.place(x=80, y=540)
output8.place(x=160, y=540)
output10.place(x=240, y=540)
output16.place(x=330, y=540)

# поле для виведення
output_data = Entry(root, bd=5, font=('Comic Sans MS', 17, 'italic'), width=30, justify='c')
output_data.place(y=610, relx=0.5, anchor='c')

# кнопка конвертації
convert_btn = Button(root, bg='#9ACD32', activebackground='#9ACD32', bd=5, text='Convert',
                     font=('Comic Sans MS', 18, 'italic', 'bold'),
                     command=convert)
convert_btn.place(y=490, relx=0.5, anchor='c')

# кнопка очищення полів вводу і виведення
clear_fields_btn = Button(root, bd=5, bg='#B0CCFF', activebackground='#B0CCFF', text='Сlear fields',
                          font=('Bahnschrift SemiBold', 13),
                          command=clear_all)
clear_fields_btn.place(x=30, y=720)

# кнопка показу історії переведень
show_btn = Button(root, bd=5, bg='#FFA07A', activebackground='#FFA07A', text='Show operations',
                  font=('Bahnschrift SemiBold', 14), command=show)
show_btn.place(x=315, y=650, anchor='ne')

# кнопка зберігання історії переведень
save_btn = Button(root, bd=5, bg='#B0CCFF', activebackground='#B0CCFF', text='Save to File',
                  font=('Bahnschrift SemiBold', 13),
                  command=save_to_file)
save_btn.place(x=425, y=720, anchor='ne')

load_btn = Button(root, bd=5, bg='#B0CCFF', activebackground='#B0CCFF', text='Load from File',
                  font=('Bahnschrift SemiBold', 13),
                  command=load_from_file)
load_btn.place(x=425, y=770, anchor='ne')

# кнопка очищення історії переведень
clear_history_btn = Button(root, bd=5, bg='#B0CCFF', activebackground='#B0CCFF', text='Clear the history',
                           font=('Bahnschrift SemiBold', 13),
                           command=clear_history)
clear_history_btn.place(x=30, y=770)

root.mainloop()
