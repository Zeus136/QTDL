def main_app():
    import tkinter as tk
    import customtkinter as ctk
    from PIL import ImageTk, Image

    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry('600x440')
    app.title("Đăng ký") 

    # Tải và đặt hình nền
    img1 = ImageTk.PhotoImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\pattern.png"))
    l1 = ctk.CTkLabel(app, image=img1)
    l1.pack()

    # Tạo khung chứa form đăng ký
    frame = ctk.CTkFrame(l1, width=302, height=370, corner_radius=15, bg_color="#242424")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    imgregister = ImageTk.PhotoImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\register.png"))
    l2 = ctk.CTkLabel(frame, image=imgregister, text="")
    l2.place(x=135, y=10)

    imguser = ctk.CTkImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\user.png"), size=(20, 20))
    l3 = ctk.CTkLabel(frame, image=imguser, text="")
    l3.place(x=20, y=67)

    imgpass = ctk.CTkImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\pass.png"), size=(20, 20))
    l4 = ctk.CTkLabel(frame, image=imgpass, text="")
    l4.place(x=20, y=127)

    imgpassconfirm = ctk.CTkImage(Image.open(r"D:\Study\HK I 2024\QTDL\Demo\assets\passconfirm.png"), size=(20, 20))
    l5 = ctk.CTkLabel(frame, image=imgpassconfirm, text="")
    l5.place(x=20, y=187)
    entry1 = ctk.CTkEntry(frame, width=220, placeholder_text="Username")
    entry1.place(x=50, y=70)

    # Tạo nhãn hiển thị lỗi cho Username
    username_error_label = ctk.CTkLabel(frame, text="", font=("Century Gothic", 8), text_color="red")
    username_error_label.place(x=50, y=100)

    entry2 = ctk.CTkEntry(frame, width=220, placeholder_text="Password", show="*")
    entry2.place(x=50, y=130)

    # Tạo nhãn hiển thị lỗi cho Password
    password_error_label = ctk.CTkLabel(frame, text="", font=("Century Gothic", 8), text_color="red")
    password_error_label.place(x=50, y=160)

    entry3 = ctk.CTkEntry(frame, width=220, placeholder_text="Confirm Password", show="*")
    entry3.place(x=50, y=190)

    # Tạo nhãn hiển thị lỗi cho Confirm Password
    confirm_password_error_label = ctk.CTkLabel(frame, text="", font=("Century Gothic", 8), text_color="red")
    confirm_password_error_label.place(x=50, y=220)

    # Tải hình ảnh show và hide sử dụng CTkImage
    show_icon_path = r"D:\Study\HK I 2024\QTDL\Demo\assets\show.png"
    hide_icon_path = r"D:\Study\HK I 2024\QTDL\Demo\assets\hide.png"
    show_icon = ctk.CTkImage(Image.open(show_icon_path), size=(14, 14))
    hide_icon = ctk.CTkImage(Image.open(hide_icon_path), size=(14, 14))

    # Trạng thái ban đầu của hai trường mật khẩu
    is_password_hidden = False
    is_confirm_password_hidden = False

    # Hàm chuyển đổi ẩn/hiện cho trường mật khẩu
    def toggle_password_visibility_1():
        global is_password_hidden
        if is_password_hidden:
            entry2.configure(show="*")
            toggle_button_1.configure(image=hide_icon)
        else:
            entry2.configure(show="")
            toggle_button_1.configure(image=show_icon)
        is_password_hidden = not is_password_hidden

    # Hàm chuyển đổi ẩn/hiện cho trường xác nhận mật khẩu
    def toggle_password_visibility_2():
        global is_confirm_password_hidden
        if is_confirm_password_hidden:
            entry3.configure(show="*")
            toggle_button_2.configure(image=hide_icon)
        else:
            entry3.configure(show="")
            toggle_button_2.configure(image=show_icon)
        is_confirm_password_hidden = not is_confirm_password_hidden

    # Nút ẩn/hiện mật khẩu cho từng trường
    toggle_button_1 = ctk.CTkButton(
        frame, 
        image=hide_icon, 
        width=15, 
        height=15, 
        command=toggle_password_visibility_1, 
        fg_color="transparent",  
        hover_color="light gray",
        text=""
    )
    toggle_button_1.place(x=270, y=133)

    toggle_button_2 = ctk.CTkButton(
        frame, 
        image=hide_icon, 
        width=15, 
        height=15, 
        command=toggle_password_visibility_2, 
        fg_color="transparent",  
        hover_color="light gray",
        text=""
    )
    toggle_button_2.place(x=270, y=193)

    # Kiểm tra tính hợp lệ của tên tài khoản và mật khẩu
    import mysql.connector
    import bcrypt

    def check_validity():
        # Xóa thông báo lỗi cũ
        username_error_label.configure(text="")
        password_error_label.configure(text="")
        confirm_password_error_label.configure(text="")

        # Lấy dữ liệu từ các ô nhập
        username = entry1.get()
        password = entry2.get()
        confirm_password = entry3.get()

        # Kiểm tra từng trường và cập nhật thông báo lỗi nếu có
        valid = True
        if len(username) == 0:
            username_error_label.configure(text="Vui lòng nhập tên đăng nhập!")
            valid = False
        if not username.isalnum():
            username_error_label.configure(text="Tên đăng nhập chỉ chứa chữ cái và số!")
            valid = False
        if len(password) < 8:
            password_error_label.configure(text="Mật khẩu phải có ít nhất 8 ký tự!")
            valid = False
        elif password != confirm_password:
            confirm_password_error_label.configure(text="Mật khẩu không khớp!")
            valid = False

        # Nếu mọi thứ hợp lệ, kiểm tra tên đăng nhập có tồn tại không
        if valid:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="130603",
                    database="qltv"  # Tên cơ sở dữ liệu của bạn
                )
                cursor = db.cursor()

                # Kiểm tra tên đăng nhập đã tồn tại
                cursor.execute("SELECT COUNT(*) FROM Users WHERE username = %s", (username,))
                count = cursor.fetchone()[0]

                if count > 0:
                    username_error_label.configure(text="Tên đăng nhập đã tồn tại!")
                    valid = False
                else:
                    # Mã hóa mật khẩu trước khi lưu
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                    # Thêm người dùng vào cơ sở dữ liệu
                    cursor.execute("INSERT INTO Users (username, password, email, role) VALUES (%s, %s, %s, %s)",
                                (username, hashed_password.decode('utf-8'), "example@example.com", "user"))  # Thay đổi email cho phù hợp
                    db.commit()
                    tk.messagebox.showinfo("Thành công", "Tài khoản đã được tạo thành công!")

            except mysql.connector.Error as err:
                print(f"Lỗi: {err}")
                tk.messagebox.showerror("Lỗi", "Không thể lưu thông tin người dùng vào cơ sở dữ liệu.")
            finally:
                cursor.close()
                db.close()


    # Hàm xóa thông báo lỗi khi người dùng nhập lại
    def clear_password_error(event):
        password_error_label.configure(text="")
        confirm_password_error_label.configure(text="")

    # Gắn sự kiện xóa lỗi khi bắt đầu nhập lại mật khẩu
    entry2.bind("<Key>", clear_password_error)
    entry3.bind("<Key>", clear_password_error)

    # Hàm xóa thông báo lỗi khi người dùng nhập lại tên người dùng
    def clear_username_error(event):
        username_error_label.configure(text="")

    # Gắn sự kiện xóa lỗi khi bắt đầu nhập lại tên người dùng
    entry1.bind("<Key>", clear_username_error)

    button1 = ctk.CTkButton(frame, text="Đăng ký", width=220, height=40, command=check_validity)
    button1.place(x=50, y=250)

    # Tạo nút đăng nhập và chuyển sang trang đăng nhập
    def switch_to_login():
        app.destroy()
        import dangnhap
        dangnhap.main_app()

    l3 = ctk.CTkLabel(frame, text="Đã có tài khoản?", font=("Century Gothic", 10))
    l3.place(x=180, y=300)

    button2 = ctk.CTkButton(frame, text="Đăng nhập", width=80, height=25, command=switch_to_login)
    button2.place(x=180, y=330)

    # Bắt hành động ấn phím Enter
    app.bind('<Return>', lambda event=None: button1.invoke())

    app.mainloop()

if __name__ == "__main__":
    main_app()