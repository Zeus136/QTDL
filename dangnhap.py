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
    frame = ctk.CTkFrame(l1, width=302, height=325, corner_radius=15, bg_color="#242424")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    imglogin = ImageTk.PhotoImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\login.png"))
    l2 = ctk.CTkLabel(frame, image=imglogin, text="")
    l2.place(x=135, y=20)

    imguser = ctk.CTkImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\user.png"), size=(20, 20))
    l3 = ctk.CTkLabel(frame, image=imguser, text="")
    l3.place(x=20, y=85)
    entry1 = ctk.CTkEntry(frame, width=220, placeholder_text="Username")
    entry1.place(x=50, y=85)

    imgpass = ctk.CTkImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\pass.png"), size=(20, 20))
    l4 = ctk.CTkLabel(frame, image=imgpass, text="")
    l4.place(x=20, y=137)
    entry2 = ctk.CTkEntry(frame, width=220, placeholder_text="Password", show="*")
    entry2.place(x=50, y=140)

    # Tải hình ảnh show và hide sử dụng CTkImage
    show_icon_path = r"D:\Study\HK I 2024\QTDL\Demo\assets\show.png"
    hide_icon_path = r"D:\Study\HK I 2024\QTDL\Demo\assets\hide.png"
    show_icon = ctk.CTkImage(Image.open(show_icon_path), size=(14, 14))
    hide_icon = ctk.CTkImage(Image.open(hide_icon_path), size=(14, 14))

    # Trạng thái ban đầu của mật khẩu (ẩn)
    hidden = True

    # Hàm chuyển đổi ẩn/hiện mật khẩu
    def toggle_password_visibility():
        nonlocal hidden
        if hidden:
            entry2.configure(show="")
            toggle_button.configure(image=hide_icon)
            hidden = False
        else:
            entry2.configure(show="*")
            toggle_button.configure(image=show_icon)
            hidden = True

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
    def main(role, username):  # Add username parameter
        if role == "admin":
            import admin
            admin.main_app(username)  # Pass username
        elif role == "user":
            import user
            user.main_app(username)  # Pass username

    def check_login():
        # Xóa thông báo lỗi cũ
        print("Starting check_login...")  # Debug print
        username_error_label.configure(text="")
        password_error_label.configure(text="")

        username = entry1.get()
        password = entry2.get()
        print("Username:", username, "Password:", password)  # Debug print

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
                print("Connecting to database...")  # Debug print
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="130603",
                    database="qltv"
                )
                cursor = db.cursor()

                cursor.callproc("DangNhap", (username, password))

                # Đọc kết quả trả về của stored procedure
                for result in cursor.stored_results():
                    output = result.fetchall()
                    print("Procedure result:", output)  # Debug print
                    if output:
                        role, thongBao = output[0]  # Lấy giá trị từ hàng đầu tiên
                        print("Role:", role, "ThongBao:", thongBao)  # Debug print

                # Xử lý kết quả đăng nhập
                if thongBao == 'Đăng nhập thành công':
                    print("Login successful")  # Debug print
                    tk.messagebox.showinfo("Thông báo", "Đăng nhập thành công.")
                    app.destroy()
                    if role == "admin" or role == "NhanVien":
                        import admin
                        admin.main_app(username, role)
                    elif role == "DocGia":
                        import user
                        user.main_app(username, role)
                else:
                    if thongBao == 'Tên đăng nhập không tồn tại':
                        username_error_label.configure(text="Tên đăng nhập không tồn tại.")
                    elif thongBao == 'Mật khẩu không đúng':
                        password_error_label.configure(text="Mật khẩu không đúng.")

            except mysql.connector.Error as err:
                print(f"Database connection error: {err}")  # Debug print
                tk.messagebox.showerror("Lỗi", f"Không thể kết nối đến cơ sở dữ liệu: {err}")
                
            finally:
                if db.is_connected():
                    cursor.close()
                    db.close()
                    print("Database connection closed.")  # Debug print

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
