def main_app():
    import tkinter as tk
    import customtkinter as ctk
    from PIL import Image, ImageTk
    import bcrypt
    import mysql.connector

    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")


    app = ctk.CTk()
    app.geometry('600x440')
    app.title("Đăng nhập")

    # Tải và đặt hình nền
    img1 = ImageTk.PhotoImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\pattern.png"))
    l1 = ctk.CTkLabel(app, image=img1)
    l1.pack()

    # Tạo khung chứa form đăng nhập
    frame = ctk.CTkFrame(l1, width=302, height=325, corner_radius=15,bg_color="#242424")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    imglogin = ImageTk.PhotoImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\login.png"))
    l2 = ctk.CTkLabel(frame, image=imglogin, text ="")
    l2.place(x=135, y=20)

    imguser = ctk.CTkImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\user.png"), size=(20, 20))
    l3 = ctk.CTkLabel(frame, image=imguser, text ="")
    l3.place(x=20, y=85)
    entry1 = ctk.CTkEntry(frame, width=220, placeholder_text="Username")
    entry1.place(x=50, y=85)
    imgpass = ctk.CTkImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\pass.png"), size=(20, 20))
    l4 = ctk.CTkLabel(frame, image=imgpass, text ="")
    l4.place(x=20, y=137)
    entry2 = ctk.CTkEntry(frame, width=220, placeholder_text="Password", show="*")
    entry2.place(x=50, y=140)

    # Tải hình ảnh show và hide sử dụng CTkImage
    show_icon_path = r"D:\Study\HK I 2024\QTDL\Demo\assets\show.png"
    hide_icon_path = r"D:\Study\HK I 2024\QTDL\Demo\assets\hide.png"
    show_icon = ctk.CTkImage(Image.open(show_icon_path), size=(14, 14))
    hide_icon = ctk.CTkImage(Image.open(hide_icon_path), size=(14, 14))

    # Trạng thái ban đầu của mật khẩu (ẩn)
    is_password_hidden = True

    # Hàm chuyển đổi ẩn/hiện mật khẩu
    def toggle_password_visibility():
        global is_password_hidden
        if is_password_hidden:
            entry2.configure(show="")
            toggle_button.configure(image=hide_icon)
            is_password_hidden = False
        else:
            entry2.configure(show="*")
            toggle_button.configure(image=show_icon)
            is_password_hidden = True

    # Nút ẩn/hiện mật khẩu
    toggle_button = ctk.CTkButton(
        frame, 
        image=show_icon, 
        width=15, 
        height=15, 
        command=toggle_password_visibility, 
        fg_color="transparent",  
        hover_color="light gray",
        text=""
    )
    toggle_button.place(x=270, y=142)


    # Tạo nhãn hiển thị lỗi cho tên đăng nhập và mật khẩu
    username_error_label = ctk.CTkLabel(frame, text="", font=("Century Gothic", 10), text_color="red", bg_color="transparent")
    username_error_label.place(x=50, y=112)

    password_error_label = ctk.CTkLabel(frame, text="", font=("Century Gothic", 10), text_color="red", bg_color="transparent")
    password_error_label.place(x=50, y=167)

    # Hàm kiểm tra tính hợp lệ của đăng nhập
    import tkinter as tk
    import customtkinter as ctk
    import mysql.connector
    import bcrypt
    
    def main(role, username):  # Add username parameter
        if role == "admin":
            import admin
            admin.main_app(username)  # Pass username
        elif role == "user":
            import user
            user.main_app(username)  # Pass username

    def check_login():
        # Xóa thông báo lỗi cũ
        username_error_label.configure(text="")
        password_error_label.configure(text="")

        username = entry1.get()
        password = entry2.get()
        
        # Kiểm tra thông tin
        valid = True
        if not username:
            username_error_label.configure(text="Vui lòng nhập tên đăng nhập.")
            valid = False
        if not password:
            password_error_label.configure(text="Vui lòng nhập mật khẩu.")
            valid = False

        if valid:
            # Kết nối đến cơ sở dữ liệu
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="130603",
                    database="qltv"
                )
                cursor = db.cursor()

                # Truy vấn để lấy mật khẩu đã mã hóa và vai trò của người dùng
                cursor.execute("SELECT password, role FROM Users WHERE username = %s", (username,))
                result = cursor.fetchone()

                if result:
                    hashed_password, role = result
                    # So sánh mật khẩu đã nhập với mật khẩu đã lưu
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                        app.destroy()
                        # Chuyển đến trang chính của ứng dụng
                        main(role, username)  # Pass username
                    else:
                        password_error_label.configure(text="Tên đăng nhập hoặc mật khẩu không chính xác!")
                else:
                    username_error_label.configure(text="Tên người dùng không tồn tại!")

            except mysql.connector.Error as err:
                print(f"Lỗi kết nối cơ sở dữ liệu: {err}")
                tk.messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
            finally:
                cursor.close()
                db.close()


    button1 = ctk.CTkButton(frame, text="Đăng nhập", width=220, height=40, command=check_login)
    button1.place(x=50, y=200)

    l3 = ctk.CTkLabel(frame, text="Chưa có tài khoản?", font=("Century Gothic", 10))
    l3.place(x=170, y=240)

    def switch_to_register():
        app.destroy()
        import dangky
        dangky.main_app()

    button2 = ctk.CTkButton(frame, text="Đăng ký", width=80, height=25, command=switch_to_register)
    button2.place(x=177, y=270)

    # Bắt sự kiện nhấn phím Enter
    app.bind('<Return>', lambda event=None: check_login())

    app.mainloop()
    
if __name__ == "__main__":
    main_app()