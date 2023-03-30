from tkinter import*
import hashlib
import psycopg2
import math

if __name__ == '__main__':
    try:
        conn = psycopg2.connect(host="127.0.0.1",
                                database="bookstore",
                                user="postgres",
                                password="147258")
        cur = conn.cursor()
    except(Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


# 库存书籍查询页面
def stock_select(cur, username):
    root = Tk()
    root.title('库存书籍查询')
    root.geometry("800x600+320+120")
    label = Label(root, text="库存书籍查询", font=("华文行楷", 20), fg="black")
    label.pack()
    label = Label(root, text="书籍信息类型", font=("华文行楷", 17), fg="black")
    label.place(x=330, y=90)
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), stock_admin(cur, username)])
    button.place(x=550, y=520)
    var = StringVar()
    var.set('book_id')
    c1 = Radiobutton(root, text="书籍编号", variable=var, value='book_id', width=5)
    c1.place(x=150, y=130)
    c2 = Radiobutton(root, text="ISBN", variable=var, value='isbn', width=5)
    c2.place(x=240, y=130)
    c3 = Radiobutton(root, text="书籍名称", variable=var, value='book_name', width=5)
    c3.place(x=330, y=130)
    c4 = Radiobutton(root, text="出版社", variable=var, value='publisher', width=5)
    c4.place(x=420, y=130)
    c5 = Radiobutton(root, text="作者", variable=var, value='author', width=5)
    c5.place(x=510, y=130)

    label = Label(root, text="书籍信息内容", font=("华文行楷", 17), fg="black")
    label.place(x=330, y=180)
    book_info = StringVar()
    entry = Entry(root, textvariable=book_info, width=40)
    entry.place(x=260, y=230)

    def callback():
        if var.get() == 'book_id':
            cur.execute("SELECT* from Stock where book_id = %s;", [book_info.get()])
        if var.get() == 'isbn':
            cur.execute("SELECT* from Stock where isbn = %s;", [book_info.get()])
        if var.get() == 'book_name':
            cur.execute("SELECT* from Stock where book_name = %s;", [book_info.get()])
        if var.get() == 'publisher':
            cur.execute("SELECT* from Stock where publisher = %s;", [book_info.get()])
        if var.get() == 'author':
            cur.execute("SELECT* from Stock where author = %s;", [book_info.get()])
        book_tuples = cur.fetchall()
        list_name = '书籍编号     ISBN      书籍名称      出版社       作者     零售价   库存量'
        label = Label(root, text=list_name, font=("华文行楷", 14), fg="black", bg="white")
        label.place(x=45, y=320)
        count = 0
        book_list = []
        for i in book_tuples:
                book_list.append(i[0]+' ')  # book_id
                book_list.append(i[1]+' ')  # isbn
                book_list.append(i[2]+' '*(10-len(i[2])))  # book_name
                book_list.append(i[3]+' '*(10-len(i[3])))  # publisher
                book_list.append(i[4]+' '*(10-len(i[4])))  # author
                book_list.append(str(i[5])+'  ')  # retail_price
                book_list.append(str(i[6]))  # stocknum
        for i in range(len(book_list)):
            if (i+1) % 7 == 0:
                count += 20
                book_result = " ".join(str(j) for j in book_list[i-6:i+1])
                label = Label(root, text=book_result, font=("华文行楷", 10), fg="black", bg="white")
                label.place(x=45, y=325+count)
    button = Button(root, text='查询', height=1, width=15, command=callback)
    button.place(x=330, y=265)
    root.mainloop()


# 书籍信息修改页面
def stock_update(cur, username):
    root = Tk()
    root.title('书籍信息修改')
    root.geometry("800x600+320+120")
    label = Label(root, text="书籍信息修改", font=("华文行楷", 20), fg="black")
    label.pack()
    label = Label(root, text="待更改书籍信息类型", font=("华文行楷", 17), fg="black")
    label.place(x=300, y=90)
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), stock_admin(cur, username)])
    button.place(x=550, y=520)
    var = StringVar()
    r1 = Radiobutton(root, text="书籍编号", variable=var, value='book_id', width=5)
    r1.place(x=150, y=130)
    r2 = Radiobutton(root, text="ISBN", variable=var, value='isbn', width=5)
    r2.place(x=240, y=130)
    r3 = Radiobutton(root, text="书籍名称", variable=var, value='book_name', width=5)
    r3.place(x=330, y=130)
    r4 = Radiobutton(root, text="出版社", variable=var, value='publisher', width=5)
    r4.place(x=420, y=130)
    r5 = Radiobutton(root, text="作者", variable=var, value='author', width=5)
    r5.place(x=510, y=130)
    label = Label(root, text="书籍编号", font=("华文行楷", 17), fg="black")
    label.place(x=190, y=185)
    book_id = StringVar()
    entry = Entry(root, textvariable=book_id, width=40)
    entry.place(x=290, y=190)
    label = Label(root, text="新书籍信息内容", font=("华文行楷", 17), fg="black")
    label.place(x=115, y=225)
    book_info = StringVar()
    entry = Entry(root, textvariable=book_info, width=40)
    entry.place(x=290, y=230)

    def callback():
        cur.execute("select* from Stock where book_id = %s;", [book_id.get()])
        target_book = cur.fetchall()
        if target_book:
            if var.get() == 'book_id':
                label = Label(root, text="禁止修改书籍编号！", font=("华文行楷", 17), fg="black")
                label.place(x=320, y=330)
            if var.get() == 'isbn':
                cur.execute("update Stock set isbn = %s where book_id = %s;", [book_info.get(), book_id.get()])
                label = Label(root, text="修改成功！", font=("华文行楷", 17), fg="black")
                label.place(x=325, y=330)
            if var.get() == 'book_name':
                cur.execute("update Stock set book_name = %s where book_id = %s;", [book_info.get(), book_id.get()])
                label = Label(root, text="修改成功！", font=("华文行楷", 17), fg="black")
                label.place(x=325, y=330)
            if var.get() == 'publisher':
                cur.execute("update Stock set publisher = %s where book_id = %s;", [book_info.get(), book_id.get()])
                label = Label(root, text="修改成功！", font=("华文行楷", 17), fg="black")
                label.place(x=325, y=330)
            if var.get() == 'author':
                cur.execute("update Stock set author = %s where book_id = %s;", [book_info.get(), book_id.get()])
                label = Label(root, text="修改成功！", font=("华文行楷", 17), fg="black")
                label.place(x=325, y=330)
        else:
            label = Label(root, text="修改失败！", font=("华文行楷", 17), fg="black")
            label.place(x=325, y=330)
    button = Button(root, text='修改', height=1, width=15, command=callback)
    button.place(x=330, y=275)
    root.mainloop()


# 买书页面
def buy_book(cur, username):
    root = Tk()
    root.title('购买书籍')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="购买书籍", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), stock_admin(cur, username)])
    button.place(x=500, y=450)
    label = Label(root, text="书籍编号", font=("华文行楷", 15), fg="black")
    label.place(x=170, y=120)
    book_id = StringVar()
    entry = Entry(root, textvariable=book_id, width=20)
    entry.place(x=280, y=120)
    label = Label(root, text="购买数量", font=("华文行楷", 15), fg="black")
    label.place(x=170, y=150)
    buy_num = IntVar()
    entry = Entry(root, textvariable=buy_num, width=20)
    entry.place(x=280, y=150)

    def callback():
        cur.execute("select current_stocknum from stock where book_id = %s", [book_id.get()])
        current_stock = cur.fetchall()
        if len(current_stock) == 0:
            label = Label(root, text="该书籍不存在，购买失败！", font=("华文行楷", 18), fg="black")
            label.place(x=200, y=230)
        elif current_stock[0][0] < buy_num.get():
            label = Label(root, text="库存不足，购买失败！", font=("华文行楷", 18), fg="black")
            label.place(x=200, y=230)
        else:
            cur.execute("update stock set current_stocknum = current_stocknum - %s where book_id = %s", [buy_num.get(), book_id.get()])
            cur.execute("select count(trading_id) from bill;")
            bill_num = cur.fetchall()
            trading_id = 'T' + '0' * (5 - len(str(bill_num[0][0]))) + str(bill_num[0][0])
            cur.execute("update bill set trading_id = %s where trading_id = 'Txxxxx'", [trading_id])
            label = Label(root, text="购买成功！", font=("华文行楷", 18), fg="black")
            label.place(x=260, y=230)
    button = Button(root, text='购买', height=1, width=15, command=callback)
    button.place(x=300, y=190)

    root.mainloop()


# 库存书籍管理页面
def stock_admin(cur, username):
    root = Tk()
    root.title('库存书籍管理')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="库存书籍管理", font=("华文行楷", 20), fg="black")
    label.pack()
    cur.execute("SELECT SU_Name from SuperUser;")
    su_name_tuple = cur.fetchall()
    su_name = [i[0] for i in su_name_tuple]
    if username in su_name:
        button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), super_login_successful(username)])
    else:
        button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), normal_login_successful(username)])
    button.place(x=500, y=450)

    def callback():
        root.destroy()
        stock_select(cur, username)  # 库存书籍查询页面
    button = Button(root, text='库存书籍查询', height=1, width=15, command=callback)
    button.place(x=120, y=200)

    def callback():
        root.destroy()
        stock_update(cur, username)  # 书籍信息修改页面
    button = Button(root, text='书籍信息修改', height=1, width=15, command=callback)
    button.place(x=290, y=200)

    def callback():
        root.destroy()
        buy_book(cur, username)  # 买书页面
    button = Button(root, text='购买书籍', height=1, width=15, command=callback)
    button.place(x=460, y=200)
    root.mainloop()


# 添加进货页面
def purchaselist_add(cur, username):
    root = Tk()
    root.title('添加进货')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="添加进货", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), book_purchase_admin(cur, username)])
    button.place(x=500, y=450)
    label = Label(root, text="书籍编号", font=("华文行楷", 13), fg="black")
    label.place(x=50, y=75)
    book_id = StringVar()
    entry = Entry(root, textvariable=book_id, width=12)
    entry.place(x=130, y=80)
    label = Label(root, text="进货价格", font=("华文行楷", 13), fg="black")
    label.place(x=230, y=75)
    purchase_price = DoubleVar()
    entry = Entry(root, textvariable=purchase_price, width=12)
    entry.place(x=310, y=80)
    label = Label(root, text="购买数量", font=("华文行楷", 13), fg="black")
    label.place(x=410, y=75)
    purchase_num = IntVar()
    entry = Entry(root, textvariable=purchase_num, width=12)
    entry.place(x=490, y=80)

    def callback():
        cur.execute("select* from Stock where book_id = %s", [book_id.get()])
        book_tuple = cur.fetchall()
        purchase_price_value = purchase_price.get()
        purchase_price_value = ('%.2f' % purchase_price_value)
        if len(book_tuple) == 0:
            label = Label(root, text="该书籍未入库，请填写下方信息", font=("华文行楷", 13), fg="black")
            label.place(x=230, y=160)
            label = Label(root, text="ISBN", font=("华文行楷", 13), fg="black")
            label.place(x=200, y=190)
            isbn = StringVar()
            entry = Entry(root, textvariable=isbn, width=20)
            entry.place(x=270, y=190)
            label = Label(root, text="书籍名称", font=("华文行楷", 13), fg="black")
            label.place(x=190, y=220)
            book_name = StringVar()
            entry = Entry(root, textvariable=book_name, width=20)
            entry.place(x=270, y=220)
            label = Label(root, text="出版社", font=("华文行楷", 13), fg="black")
            label.place(x=200, y=250)
            publisher = StringVar()
            entry = Entry(root, textvariable=publisher, width=20)
            entry.place(x=270, y=250)
            label = Label(root, text="作者", font=("华文行楷", 13), fg="black")
            label.place(x=200, y=280)
            author = StringVar()
            entry = Entry(root, textvariable=author, width=20)
            entry.place(x=270, y=280)
            label = Label(root, text="零售价", font=("华文行楷", 13), fg="black")
            label.place(x=200, y=310)
            retail_price = DoubleVar()
            entry = Entry(root, textvariable=retail_price, width=20)
            entry.place(x=270, y=310)

            def callback():
                cur.execute("select count(purchase_id) from purchaselist;")
                purchaselist_num = cur.fetchall()
                retail_price_value = retail_price.get()
                retail_price_value = ('%.2f' % retail_price_value)
                purchase_id = 'P' + '0' * (5 - len(str(purchaselist_num[0][0]))) + str(purchaselist_num[0][0]+1)
                cur.execute("call insert_purchaseList(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", [purchase_id, book_id.get(), isbn.get(),
                                                                                      book_name.get(), publisher.get(), author.get(), retail_price_value,
                                                                                      purchase_price_value, purchase_num.get(), '未付款'])
                cur.execute("select* from purchaselist where purchase_id = %s", [purchase_id])
                purchase_tuple = cur.fetchall()
                if len(purchase_tuple) != 0:
                    label = Label(root, text="添加成功！", font=("华文行楷", 15), fg="black")
                    label.place(x=270, y=390)
            button = Button(root, text='重新添加', height=1, width=20, command=callback)
            button.place(x=275, y=350)
        else:   # 该书籍在库存中出现过
            cur.execute("select count(purchase_id) from purchaselist;")
            purchaselist_num = cur.fetchall()
            purchase_id = 'P' + '0' * (5 - len(str(purchaselist_num[0][0]))) + str(purchaselist_num[0][0]+1)
            cur.execute("call insert_purchaseList(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                        [purchase_id, book_id.get(), book_tuple[0][1], book_tuple[0][2],
                         book_tuple[0][3], book_tuple[0][4], book_tuple[0][5], purchase_price_value, purchase_num.get(), '未付款'])
            cur.execute("select* from purchaselist where purchase_id = %s", [purchase_id])
            purchase_tuple = cur.fetchall()
            if len(purchase_tuple) != 0:
                label = Label(root, text="添加成功！", font=("华文行楷", 15), fg="black")
                label.place(x=290, y=210)
    button = Button(root, text='添加', height=1, width=20, command=callback)
    button.place(x=280, y=120)

    root.mainloop()


# 书籍进货管理页面
def book_purchase_admin(cur, username):
    root = Tk()
    root.title('书籍进货管理')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="书籍进货管理", font=("华文行楷", 20), fg="black")
    label.pack()
    cur.execute("SELECT SU_Name from SuperUser;")
    su_name_tuple = cur.fetchall()
    su_name = [i[0] for i in su_name_tuple]
    if username in su_name:
        button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), super_login_successful(username)])
    else:
        button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), normal_login_successful(username)])
    button.place(x=500, y=450)
    label = Label(root, text="进货清单编号", font=("华文行楷", 15), fg="black")
    label.place(x=130, y=75)
    purchase_id = StringVar()
    entry = Entry(root, textvariable=purchase_id, width=30)
    entry.place(x=270, y=80)

    def lookup():
        cur.execute("select* from purchaselist where purchase_id = %s", [purchase_id.get()])
        purchase_tuple = cur.fetchall()
        list_name = '清单编号  书籍编号   ISBN    书籍名称     出版社      作者    零售价   进货价   购买数量  状态'
        label = Label(root, text=list_name, font=("华文行楷", 10), fg="black", bg="white")
        label.place(x=30, y=170)
        purchase_list = []
        for i in purchase_tuple:
            purchase_list.append(i[0])  # purchase_id
            purchase_list.append(i[1])  # book_id
            purchase_list.append(i[2])  # isbn
            purchase_list.append(i[3])  # book_name
            purchase_list.append(i[4])  # publisher
            purchase_list.append(i[5])  # author
            purchase_list.append(str(i[6]))  # retail_price
            purchase_list.append(str(i[7]))  # purchase_price
            purchase_list.append(str(i[8]))  # purchase_num
            purchase_list.append(i[9])  # status
            purchase_result = " ".join(str(j) for j in purchase_list)
            label = Label(root, text=purchase_result, font=("华文行楷", 9), fg="black", bg="white")
            label.place(x=25, y=185)
        return purchase_list
    button = Button(root, text='查看', height=1, width=10, command=lookup)
    button.place(x=310, y=120)

    def callback():
        purchase_list = lookup()
        if purchase_list[9] == '未付款':
            cur.execute("update purchaselist set status = '已付款' where purchase_id = %s", [purchase_list[0]])
            cur.execute("select count(trading_id) from bill;")
            bill_num = cur.fetchall()
            trading_id = 'T' + '0' * (5 - len(str(bill_num[0][0]))) + str(bill_num[0][0])
            cur.execute("update bill set trading_id = %s where trading_id = 'Txxxxx'", [trading_id])
            label = Label(root, text='付款成功！', font=("华文行楷", 15), fg="black")
            label.place(x=310, y=280)
        else:
            label = Label(root, text='付款失败！', font=("华文行楷", 15), fg="black")  # 如果该进货书籍已付款或已退货或已入库，则不能进行付款操作
            label.place(x=310, y=280)
    button = Button(root, text='付款', height=1, width=10, command=callback)
    button.place(x=130, y=230)

    def callback():
        purchase_list = lookup()
        if purchase_list[9] != '未付款':
            label = Label(root, text='退货失败！', font=("华文行楷", 15), fg="black")  # 如果该进货书籍已付款或已退货或已入库，则不能进行退货操作
            label.place(x=310, y=280)
        else:
            cur.execute("update purchaselist set status = '已退货' where purchase_id = %s", [purchase_list[0]])
            label = Label(root, text='退货成功！', font=("华文行楷", 15), fg="black")
            label.place(x=310, y=280)
    button = Button(root, text='退货', height=1, width=10, command=callback)
    button.place(x=250, y=230)

    def callback():
        purchase_list = lookup()
        if purchase_list[9] == '已付款':
            cur.execute("update purchaselist set status = '已入库' where purchase_id = %s", [purchase_list[0]])
            label = Label(root, text='入库成功！', font=("华文行楷", 15), fg="black")
            label.place(x=310, y=280)
        else:
            label = Label(root, text='入库失败！', font=("华文行楷", 15), fg="black")  # 如果该进货书籍未付款或已退货或已入库，则不能进行入库操作
            label.place(x=310, y=280)
    button = Button(root, text='入库', height=1, width=10, command=callback)
    button.place(x=370, y=230)

    def callback():
        root.destroy()
        purchaselist_add(cur, username)  # 添加进货页面
    button = Button(root, text='添加', height=1, width=10, command=callback)
    button.place(x=490, y=230)

    root.mainloop()


# 财务账户明细查询页面
def bill_select(cur, username):
    root = Tk()
    root.title('财务账户明细查询')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="财务帐户明细查询", font=("华文行楷", 20), fg="black")
    label.pack()
    cur.execute("SELECT SU_Name from SuperUser;")
    su_name_tuple = cur.fetchall()
    su_name = [i[0] for i in su_name_tuple]
    if username in su_name:
        button = Button(root, text='返回', height=1, width=20,
                        command=lambda: [root.destroy(), bill_admin(cur, username)])
    else:
        button = Button(root, text='返回', height=1, width=20,
                        command=lambda: [root.destroy(), bill_admin(cur, username)])
    button.place(x=500, y=450)
    label = Label(root, text="待查询账单类型", font=("华文行楷", 17), fg="black")
    label.place(x=260, y=60)
    var = StringVar()
    r1 = Radiobutton(root, text="交易编号", variable=var, value='trading_id', width=5)
    r1.place(x=250, y=110)
    r2 = Radiobutton(root, text="交易时间", variable=var, value='trading_date', width=5)
    r2.place(x=350, y=110)

    def callback():  # button下一步
        label = Label(root, text="查询账单信息内容", font=("华文行楷", 17), fg="black")
        label.place(x=250, y=190)
        if var.get() == 'trading_id':
            label = Label(root, text="交易编号", font=("华文行楷", 15), fg="black")
            label.place(x=220, y=230)
            trading_id = StringVar()
            entry = Entry(root, textvariable=trading_id, width=20)
            entry.place(x=320, y=230)

            def callback():  # button查询交易编号
                cur.execute("select * from bill where trading_id = %s", [trading_id.get()])
                bill_tuple = cur.fetchall()
                list_name = "交易编号  操作   金额     交易时间   "
                label = Label(root, text=list_name, font=("华文行楷", 10), fg="black", bg="white")
                label.place(x=160, y=320)
                bill_list = []
                for i in bill_tuple:
                    bill_list.append(i[0])  # trading_id
                    bill_list.append(i[1])  # operation
                    bill_list.append(i[2])  # amount
                    bill_list.append(i[3])  # trading_date
                    bill_result = " ".join(str(j) for j in bill_list)
                    label = Label(root, text=bill_result, font=("华文行楷", 11), fg="black", bg="white")
                    label.place(x=160, y=339)
            button = Button(root, text='查询', height=1, width=10, command=callback)
            button.place(x=300, y=270)
        if var.get() == 'trading_date':
            label = Label(root, text="交易查询起始日期", font=("华文行楷", 15), fg="black")
            label.place(x=150, y=230)
            begin_year = StringVar()
            entry = Entry(root, textvariable=begin_year, width=10)
            entry.place(x=330, y=230)
            label = Label(root, text="年", font=("华文行楷", 15), fg="black")
            label.place(x=380, y=230)
            begin_month = StringVar()
            entry = Entry(root, textvariable=begin_month, width=10)
            entry.place(x=410, y=230)
            label = Label(root, text="月", font=("华文行楷", 15), fg="black")
            label.place(x=460, y=230)
            begin_day = StringVar()
            entry = Entry(root, textvariable=begin_day, width=10)
            entry.place(x=490, y=230)
            label = Label(root, text="日", font=("华文行楷", 15), fg="black")
            label.place(x=540, y=230)
            label = Label(root, text="交易查询结束日期", font=("华文行楷", 15), fg="black")
            label.place(x=150, y=260)
            end_year = StringVar()
            entry = Entry(root, textvariable=end_year, width=10)
            entry.place(x=330, y=260)
            label = Label(root, text="年", font=("华文行楷", 15), fg="black")
            label.place(x=380, y=260)
            end_month = StringVar()
            entry = Entry(root, textvariable=end_month, width=10)
            entry.place(x=410, y=260)
            label = Label(root, text="月", font=("华文行楷", 15), fg="black")
            label.place(x=460, y=260)
            end_day = StringVar()
            entry = Entry(root, textvariable=end_day, width=10)
            entry.place(x=490, y=260)
            label = Label(root, text="日", font=("华文行楷", 15), fg="black")
            label.place(x=540, y=260)

            def callback():
                list_name = "交易编号    操作    金额     交易时间   "
                label = Label(root, text=list_name, font=("华文行楷", 10), fg="black", bg="white")
                label.place(x=160, y=335)
                begin_date = begin_year.get() + '-' + begin_month.get() + '-' + begin_day.get()
                end_date = end_year.get() + '-' + end_month.get() + '-' + end_day.get()
                cur.execute("select * from bill where trading_date >= %s and trading_date <= %s", [begin_date, end_date])
                bill_tuples = cur.fetchall()
                count = 0
                bill_list = []
                for i in bill_tuples:
                    bill_list.append(i[0] + '  ')  # trading_id
                    bill_list.append(i[1] + '  ')  # operation
                    bill_list.append(str(i[2]) + '  ')  # amount
                    bill_list.append(str(i[3]) + '  ')  # trading_date
                for i in range(len(bill_list)):
                    if (i + 1) % 4 == 0:
                        count += 20
                        book_result = " ".join(str(j) for j in bill_list[i - 3:i + 1])
                        label = Label(root, text=book_result, font=("华文行楷", 10), fg="black", bg="white")
                        label.place(x=160, y=335 + count)
            button = Button(root, text='查询', height=1, width=10, command=callback)
            button.place(x=300, y=295)
    button = Button(root, text='下一步', height=1, width=10, command=callback)
    button.place(x=300, y=150)

    root.mainloop()


# 财务账户净利润查询
def bill_profit(cur, username):
    root = Tk()
    root.title('财务账户净利润查询')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="财务账户净利润查询", font=("华文行楷", 20), fg="black")
    label.pack()
    cur.execute("SELECT SU_Name from SuperUser;")
    su_name_tuple = cur.fetchall()
    su_name = [i[0] for i in su_name_tuple]
    if username in su_name:
        button = Button(root, text='返回', height=1, width=20,
                        command=lambda: [root.destroy(), bill_admin(cur, username)])
    else:
        button = Button(root, text='返回', height=1, width=20,
                        command=lambda: [root.destroy(), bill_admin(cur, username)])
    button.place(x=500, y=450)
    label = Label(root, text="净利润类型", font=("华文行楷", 17), fg="black")
    label.place(x=270, y=60)
    var = StringVar()
    r1 = Radiobutton(root, text="总利润", variable=var, value='total_profit', width=8)
    r1.place(x=200, y=110)
    r2 = Radiobutton(root, text="特定交易时间段利润", variable=var, value='period_profit', width=14)
    r2.place(x=370, y=110)

    def callback():  # button下一步
        if var.get() == 'total_profit':
            cur.execute("select sum(amount) from bill where operation = %s", ['收入'])
            total_earn = cur.fetchall()
            cur.execute("select sum(amount) from bill where operation = %s", ['支出'])
            total_pay = cur.fetchall()
            total_profit = total_earn[0][0] - total_pay[0][0]
            if total_profit < 0:
                label = Label(root, text="书城共亏损", font=("华文行楷", 17), fg="black", bg="white")
                label.place(x=180, y=300)
                total_profit = abs(total_profit)
                label = Label(root, text=('%.2f' % total_profit), font=("华文行楷", 17), fg="black", bg="white")
                label.place(x=300, y=300)
            else:
                label = Label(root, text="书城共盈利", font=("华文行楷", 17), fg="black")
                label.place(x=180, y=300)
                label = Label(root, text=('%.2f' % total_profit), font=("华文行楷", 17), fg="black")
                label.place(x=300, y=300)
        if var.get() == 'period_profit':
            label = Label(root, text="查询利润内容", font=("华文行楷", 17), fg="black")
            label.place(x=250, y=190)
            label = Label(root, text="利润查询起始日期", font=("华文行楷", 15), fg="black")
            label.place(x=150, y=230)
            begin_year = StringVar()
            entry = Entry(root, textvariable=begin_year, width=10)
            entry.place(x=330, y=230)
            label = Label(root, text="年", font=("华文行楷", 15), fg="black")
            label.place(x=380, y=230)
            begin_month = StringVar()
            entry = Entry(root, textvariable=begin_month, width=10)
            entry.place(x=410, y=230)
            label = Label(root, text="月", font=("华文行楷", 15), fg="black")
            label.place(x=460, y=230)
            begin_day = StringVar()
            entry = Entry(root, textvariable=begin_day, width=10)
            entry.place(x=490, y=230)
            label = Label(root, text="日", font=("华文行楷", 15), fg="black")
            label.place(x=540, y=230)
            label = Label(root, text="利润查询结束日期", font=("华文行楷", 15), fg="black")
            label.place(x=150, y=260)
            end_year = StringVar()
            entry = Entry(root, textvariable=end_year, width=10)
            entry.place(x=330, y=260)
            label = Label(root, text="年", font=("华文行楷", 15), fg="black")
            label.place(x=380, y=260)
            end_month = StringVar()
            entry = Entry(root, textvariable=end_month, width=10)
            entry.place(x=410, y=260)
            label = Label(root, text="月", font=("华文行楷", 15), fg="black")
            label.place(x=460, y=260)
            end_day = StringVar()
            entry = Entry(root, textvariable=end_day, width=10)
            entry.place(x=490, y=260)
            label = Label(root, text="日", font=("华文行楷", 15), fg="black")
            label.place(x=540, y=260)

            def callback():
                begin_date = begin_year.get() + '-' + begin_month.get() + '-' + begin_day.get()
                end_date = end_year.get() + '-' + end_month.get() + '-' + end_day.get()
                cur.execute("select sum(amount) from bill where operation = %s and trading_date >= %s  and trading_date <= %s",
                            ['收入', begin_date, end_date])
                period_earn = cur.fetchall()
                cur.execute("select sum(amount) from bill where operation = %s and trading_date >= %s  and trading_date <= %s",
                            ['支出', begin_date, end_date])
                period_pay = cur.fetchall()
                if period_earn[0][0] and period_pay[0][0]:
                    period_profit = period_earn[0][0] - period_pay[0][0]
                elif period_pay[0][0] is None and period_earn[0][0]:
                    period_profit = period_earn[0][0] - 0
                elif period_earn[0][0] is None and period_pay[0][0]:
                    period_profit = 0 - period_pay[0][0]
                else:
                    profit = 0
                if period_profit < 0:
                    label = Label(root, text="书城共亏损", font=("华文行楷", 15), fg="black", bg="white")
                    label.place(x=195, y=360)
                    period_profit = abs(period_profit)
                    label = Label(root, text=('%.2f' % period_profit), font=("华文行楷", 15), fg="black", bg="white")
                    label.place(x=300, y=360)
                else:
                    label = Label(root, text="书城共盈利", font=("华文行楷", 15), fg="black", bg="white")
                    label.place(x=195, y=360)
                    label = Label(root, text=('%.2f' % period_profit), font=("华文行楷", 15), fg="black", bg="white")
                    label.place(x=300, y=360)
            button = Button(root, text='查询', height=1, width=10, command=callback)
            button.place(x=300, y=295)

    button = Button(root, text='下一步', height=1, width=10, command=callback)
    button.place(x=300, y=150)

    root.mainloop()


# 财务账户管理页面
def bill_admin(cur, username):
    root = Tk()
    root.title('财务账户管理')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="财务帐户管理", font=("华文行楷", 20), fg="black")
    label.pack()
    cur.execute("SELECT SU_Name from SuperUser;")
    su_name_tuple = cur.fetchall()
    su_name = [i[0] for i in su_name_tuple]
    if username in su_name:
        button = Button(root, text='返回', height=1, width=20,
                        command=lambda: [root.destroy(), super_login_successful(username)])
    else:
        button = Button(root, text='返回', height=1, width=20,
                        command=lambda: [root.destroy(), normal_login_successful(username)])
    button.place(x=500, y=450)

    def callback():
        root.destroy()
        bill_select(cur, username)
    button = Button(root, text='财务账户明细查询', height=1, width=20, command=callback)
    button.place(x=180, y=150)

    def callback():
        root.destroy()
        bill_profit(cur, username)
    button = Button(root, text='财务账户净利润查询', height=1, width=20, command=callback)
    button.place(x=370, y=150)
    root.mainloop()


#  超级用户个人信息修改页面
def SU_update(cur, username):
    root = Tk()
    root.title('超级用户个人信息修改')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="超级用户个人信息修改", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回', height=1, width=20,
                    command=lambda: [root.destroy(), SU_admin(cur, username)])
    button.place(x=500, y=450)
    label = Label(root, text="用户名", font=("华文行楷", 15), fg="black")
    label.place(x=220, y=70)
    new_username = StringVar()
    entry = Entry(root, textvariable=new_username, width=20)
    entry.place(x=290, y=70)
    label = Label(root, text="待修改信息类型", font=("华文行楷", 17), fg="black")
    label.place(x=260, y=100)
    var = StringVar()
    r1 = Radiobutton(root, text="用户名", variable=var, value='SU_id', width=5)
    r1.place(x=100, y=150)
    r2 = Radiobutton(root, text="密码", variable=var, value='SU_code', width=5)
    r2.place(x=180, y=150)
    r3 = Radiobutton(root, text="真实姓名", variable=var, value='SU_actualname', width=5)
    r3.place(x=260, y=150)
    r4 = Radiobutton(root, text="性别", variable=var, value='SU_gender', width=5)
    r4.place(x=340, y=150)
    r5 = Radiobutton(root, text="出生日期", variable=var, value='SU_birth', width=5)
    r5.place(x=420, y=150)
    r6 = Radiobutton(root, text="电话号码", variable=var, value='SU_phonenumber', width=5)
    r6.place(x=500, y=150)

    def callback():  # 下一步button
        label = Label(root, text="新个人信息内容", font=("华文行楷", 17), fg="black")
        label.place(x=260, y=200)
        if var.get() == 'SU_birth':
            label = Label(root, text="新出生日期", font=("华文行楷", 15), fg="black")
            label.place(x=200, y=240)
            birth_year = StringVar()
            entry = Entry(root, textvariable=birth_year, width=10)
            entry.place(x=330, y=240)
            label = Label(root, text="年", font=("华文行楷", 15), fg="black")
            label.place(x=380, y=240)
            birth_month = StringVar()
            entry = Entry(root, textvariable=birth_month, width=10)
            entry.place(x=410, y=240)
            label = Label(root, text="月", font=("华文行楷", 15), fg="black")
            label.place(x=460, y=240)
            birth_day = StringVar()
            entry = Entry(root, textvariable=birth_day, width=10)
            entry.place(x=490, y=240)
            label = Label(root, text="日", font=("华文行楷", 15), fg="black")
            label.place(x=540, y=240)

            def callback():
                new_birth = birth_year.get() + '-' + birth_month.get() + '-' + birth_day.get()
                cur.execute("update superuser set su_birth = %s where su_name = %s", [new_birth, username])
                label = Label(root, text="修改成功！", font=("华文行楷", 15), fg="black")
                label.place(x=280, y=320)
            button = Button(root, text='修改', height=1, width=20, command=callback)
            button.place(x=270, y=280)
        else:
            label = Label(root, text="新个人信息内容", font=("华文行楷", 15), fg="black")
            label.place(x=170, y=240)
            new_info = StringVar()
            entry = Entry(root, textvariable=new_info, width=15)
            entry.place(x=330, y=240)

            def callback():
                if var.get() == 'SU_id':
                    cur.execute("update superuser set su_id = %s where su_name = %s", [new_info.get(), username])
                elif var.get() == 'SU_code':
                    code = new_info.get()
                    code_md5 = hashlib.md5(code.encode(encoding='utf-8')).hexdigest()  # 对输入密码进行MD5加密
                    cur.execute("update superuser set su_code = %s where su_name = %s", [code_md5, username])
                elif var.get() == 'SU_actualname':
                    cur.execute("update superuser set su_actualname = %s where su_name = %s", [new_info.get(), username])
                elif var.get() == 'SU_gender':
                    cur.execute("update superuser set su_gender = %s where su_name = %s", [new_info.get(), username])
                else:  # var.get() == 'SU_phonenumber'
                    cur.execute("update superuser set su_phonenumber = %s where su_name = %s", [new_info.get(), username])
                label = Label(root, text="修改成功！", font=("华文行楷", 15), fg="black")
                label.place(x=280, y=320)
            button = Button(root, text='修改', height=1, width=20, command=callback)
            button.place(x=270, y=280)
    button = Button(root, text='下一步', height=1, width=20, command=callback)
    button.place(x=270, y=190)
    root.mainloop()

# 超级用户信息管理页面
def SU_admin(cur, username):
    root = Tk()
    root.title('超级用户信息管理')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="超级用户信息管理", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), user_admin(cur, username)])
    button.place(x=500, y=450)

    def callback():
        label = Label(root, text="用户名", font=("华文行楷", 15), fg="black")
        label.place(x=220, y=180)
        new_username = StringVar()
        entry = Entry(root, textvariable=new_username, width=20)
        entry.place(x=300, y=180)

        def callback():
            cur.execute("select * from superUser where su_name = %s", [new_username.get()])
            info_tuple = cur.fetchall()
            list_name = "用户编号   用户名        密码        真实姓名  性别  出生日期   电话号码  "
            label = Label(root, text=list_name, font=("华文行楷", 12), fg="black", bg="white")
            label.place(x=45, y=260)
            info_list = []
            for i in info_tuple:
                info_list.append(i[0])  # SU_id
                info_list.append(i[1])  # SU_name
                info_list.append(i[2])  # SU_code
                info_list.append(i[3])  # SU_actualname
                info_list.append(i[4])  # SU_gender
                info_list.append(str(i[5]))  # SU_birth
                info_list.append(i[6])  # SU_phonenumber
            info_result = " ".join(str(j) for j in info_list)
            label = Label(root, text=info_result, font=("华文行楷", 10), fg="black", bg="white")
            label.place(x=45, y=280)
        button = Button(root, text='查询', height=1, width=10, command=callback)
        button.place(x=280, y=210)
    button = Button(root, text='超级用户信息查询', height=1, width=20, command=callback)
    button.place(x=170, y=120)

    def callback():
        root.destroy()
        SU_update(cur, username)  # 超级用户信息修改页面
    button = Button(root, text='超级用户信息修改', height=1, width=20, command=callback)
    button.place(x=340, y=120)
    root.mainloop()


# 普通用户信息修改页面
def NU_update(cur, username):
    root = Tk()
    root.title('普通用户信息修改页面')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="普通用户信息修改页面", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), NU_admin(cur, username)])
    button.place(x=500, y=450)
    label = Label(root, text="待修改普通用户编号", font=("华文行楷", 15), fg="black")
    label.place(x=130, y=100)
    NU_id = StringVar()
    entry = Entry(root, textvariable=NU_id, width=13)
    entry.place(x=340, y=100)
    label = Label(root, text="待修改信息类型", font=("华文行楷", 17), fg="black")
    label.place(x=260, y=150)
    var = StringVar()
    r1 = Radiobutton(root, text="用户名", variable=var, value='NU_name', width=5)
    r1.place(x=100, y=180)
    r2 = Radiobutton(root, text="密码", variable=var, value='NU_code', width=5)
    r2.place(x=180, y=180)
    r3 = Radiobutton(root, text="真实姓名", variable=var, value='NU_actualname', width=5)
    r3.place(x=260, y=180)
    r4 = Radiobutton(root, text="性别", variable=var, value='NU_gender', width=5)
    r4.place(x=340, y=180)
    r5 = Radiobutton(root, text="出生日期", variable=var, value='NU_birth', width=5)
    r5.place(x=420, y=180)
    r6 = Radiobutton(root, text="电话号码", variable=var, value='NU_phonenumber', width=5)
    r6.place(x=500, y=180)

    def callback():  # 下一步button
        if var.get() == 'NU_birth':
            label = Label(root, text="新出生日期", font=("华文行楷", 15), fg="black")
            label.place(x=200, y=270)
            birth_year = StringVar()
            entry = Entry(root, textvariable=birth_year, width=10)
            entry.place(x=330, y=270)
            label = Label(root, text="年", font=("华文行楷", 15), fg="black")
            label.place(x=380, y=270)
            birth_month = StringVar()
            entry = Entry(root, textvariable=birth_month, width=10)
            entry.place(x=410, y=270)
            label = Label(root, text="月", font=("华文行楷", 15), fg="black")
            label.place(x=460, y=270)
            birth_day = StringVar()
            entry = Entry(root, textvariable=birth_day, width=10)
            entry.place(x=490, y=270)
            label = Label(root, text="日", font=("华文行楷", 15), fg="black")
            label.place(x=540, y=270)

            def callback():
                new_birth = birth_year.get() + '-' + birth_month.get() + '-' + birth_day.get()
                cur.execute("update normaluser set nu_birth = %s where nu_id = %s", [new_birth, NU_id.get()])
                label = Label(root, text="修改成功！", font=("华文行楷", 15), fg="black")
                label.place(x=280, y=350)
            button = Button(root, text='修改', height=1, width=20, command=callback)
            button.place(x=270, y=310)
        else:
            label = Label(root, text="新个人信息内容", font=("华文行楷", 15), fg="black")
            label.place(x=180, y=270)
            new_info = StringVar()
            entry = Entry(root, textvariable=new_info, width=20)
            entry.place(x=340, y=270)

            def callback():
                if var.get() == 'NU_name':
                    cur.execute("update normaluser set nu_name = %s where nu_id = %s", [new_info.get(), NU_id.get()])
                elif var.get() == 'NU_code':
                    code = new_info.get()
                    code_md5 = hashlib.md5(code.encode(encoding='utf-8')).hexdigest()  # 对输入密码进行MD5加密
                    cur.execute("update normaluser set nu_code = %s where nu_id = %s", [code_md5, NU_id.get()])
                elif var.get() == 'NU_actualname':
                    cur.execute("update normaluser set nu_actualname = %s where nu_id = %s",
                                [new_info.get(), NU_id.get()])
                elif var.get() == 'NU_gender':
                    cur.execute("update normaluser set nu_gender = %s where nu_id = %s", [new_info.get(), NU_id.get()])
                else:  # var.get() == 'NU_phonenumber'
                    cur.execute("update normaluser set nu_phonenumber = %s where nu_id = %s",
                                [new_info.get(), NU_id.get()])
                label = Label(root, text="修改成功！", font=("华文行楷", 15), fg="black")
                label.place(x=280, y=350)
            button = Button(root, text='修改', height=1, width=20, command=callback)
            button.place(x=270, y=310)
    button = Button(root, text='下一步', height=1, width=20, command=callback)
    button.place(x=270, y=220)
    root.mainloop()


# 普通用户添加页面
def NU_add(cur, username):
    root = Tk()
    root.title('普通用户添加')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="普通用户添加", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), user_admin(cur, username)])
    button.place(x=500, y=450)
    label = Label(root, text="普通用户信息输入", font=("华文行楷", 20), fg="black")
    label.place(x=250, y=70)
    label = Label(root, text="用户名", font=("华文行楷", 15), fg="black")
    label.place(x=150, y=120)
    nu_name = StringVar()
    entry = Entry(root, textvariable=nu_name, width=20)
    entry.place(x=300, y=120)
    label = Label(root, text="密码", font=("华文行楷", 15), fg="black")
    label.place(x=150, y=150)
    nu_code = StringVar()
    entry = Entry(root, textvariable=nu_code, width=20, show="*")
    entry.place(x=300, y=150)
    label = Label(root, text="真实姓名", font=("华文行楷", 15), fg="black")
    label.place(x=150, y=180)
    nu_actualname = StringVar()
    entry = Entry(root, textvariable=nu_actualname, width=20)
    entry.place(x=300, y=180)
    label = Label(root, text="性别", font=("华文行楷", 15), fg="black")
    label.place(x=150, y=210)
    nu_gender = StringVar()
    entry = Entry(root, textvariable=nu_gender, width=20)
    entry.place(x=300, y=210)
    label = Label(root, text="出生日期", font=("华文行楷", 15), fg="black")
    label.place(x=150, y=240)
    nu_birth_year = StringVar()
    entry = Entry(root, textvariable=nu_birth_year, width=10)
    entry.place(x=300, y=240)
    label = Label(root, text="年", font=("华文行楷", 15), fg="black")
    label.place(x=350, y=240)
    nu_birth_month = StringVar()
    entry = Entry(root, textvariable=nu_birth_month, width=10)
    entry.place(x=380, y=240)
    label = Label(root, text="月", font=("华文行楷", 15), fg="black")
    label.place(x=430, y=240)
    nu_birth_day = StringVar()
    entry = Entry(root, textvariable=nu_birth_day, width=10)
    entry.place(x=460, y=240)
    label = Label(root, text="日", font=("华文行楷", 15), fg="black")
    label.place(x=510, y=240)
    label = Label(root, text="电话号码", font=("华文行楷", 15), fg="black")
    label.place(x=150, y=270)
    nu_phonenumber = StringVar()
    entry = Entry(root, textvariable=nu_phonenumber, width=20)
    entry.place(x=300, y=270)

    def callback():
        cur.execute("select count(*) from normaluser")
        nu_num = cur.fetchall()
        nu_id = 'NU' + (4-len(str(nu_num[0][0]+1))) * '0' + str(nu_num[0][0]+1)
        code = nu_code.get()
        code_md5 = hashlib.md5(code.encode(encoding='utf-8')).hexdigest()  # 对输入密码进行MD5加密
        nu_birth = nu_birth_year.get() + '-' + nu_birth_month.get() + '-' + nu_birth_day.get()
        cur.execute("insert into normaluser values(%s,%s,%s,%s,%s,%s,%s)", [nu_id, nu_name.get(), code_md5, nu_actualname.get(),
                                                                              nu_gender.get(), nu_birth, nu_phonenumber.get()])
        label = Label(root, text="添加成功！", font=("华文行楷", 15), fg="black")
        label.place(x=320, y=350)
    button = Button(root, text='添加', height=1, width=20, command=callback)
    button.place(x=300, y=310)
    root.mainloop()


# 超级用户管理普通用户页面
def NU_admin(cur, username):
    root = Tk()
    root.title('普通用户信息管理')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="普通用户信息管理", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), user_admin(cur, username)])
    button.place(x=500, y=450)

    def callback():  # 普通用户信息查询
        label = Label(root, text="普通用户编号", font=("华文行楷", 15), fg="black")
        label.place(x=150, y=160)
        NU_id = StringVar()
        entry = Entry(root, textvariable=NU_id, width=13)
        entry.place(x=300, y=160)

        def callback():
            cur.execute("select * from NormalUser where nu_id = %s", [NU_id.get()])
            info_tuple = cur.fetchall()
            list_name = "用户编号   用户名         密码          真实姓名  性别  出生日期   电话号码  "
            label = Label(root, text=list_name, font=("华文行楷", 12), fg="black", bg="white")
            label.place(x=45, y=240)
            info_list = []
            for i in info_tuple:
                info_list.append(i[0])  # NU_id
                info_list.append(i[1])  # NU_name
                info_list.append(i[2])  # NU_code
                info_list.append(i[3])  # NU_actualname
                info_list.append(i[4])  # NU_gender
                info_list.append(str(i[5]))  # NU_birth
                info_list.append(i[6])  # NU_phonenumber
            info_result = " ".join(str(j) for j in info_list)
            label = Label(root, text=info_result, font=("华文行楷", 10), fg="black", bg="white")
            label.place(x=45, y=260)
        button = Button(root, text='查询', height=1, width=20, command=callback)
        button.place(x=270, y=200)
    button = Button(root, text='普通用户信息查询', height=1, width=20, command=callback)
    button.place(x=100, y=110)

    def callback():
        root.destroy()
        NU_update(cur, username)  # 普通用户信息修改页面
    button = Button(root, text='普通用户信息修改', height=1, width=20, command=callback)
    button.place(x=300, y=110)

    def callback():
        root.destroy()
        NU_add(cur, username)  # 普通用户添加页面
    button = Button(root, text='普通用户添加', height=1, width=20, command=callback)
    button.place(x=500, y=110)
    root.mainloop()


# 用户信息管理页面
def user_admin(cur, username):
    root = Tk()
    root.title('用户信息管理')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="用户信息管理", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), super_login_successful(username)])
    button.place(x=500, y=450)

    def callback():
        root.destroy()
        NU_admin(cur, username)  # 普通用户信息管理页面
    button = Button(root, text='普通用户信息管理', height=1, width=20, command=callback)
    button.place(x=130, y=150)

    def callback():
        root.destroy()
        SU_admin(cur, username)  # 超级用户信息管理页面
    button = Button(root, text='超级用户信息管理', height=1, width=20, command=callback)
    button.place(x=330, y=150)
    root.mainloop()


# 普通用户个人信息修改页面
def NUself_update(cur, username):
    root = Tk()
    root.title('普通用户个人信息修改页面')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="普通用户个人信息修改页面", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), NUself_admin(cur, username)])
    button.place(x=500, y=450)
    label = Label(root, text="待修改信息类型", font=("华文行楷", 17), fg="black")
    label.place(x=260, y=150)
    var = StringVar()
    r1 = Radiobutton(root, text="用户名", variable=var, value='NU_name', width=5)
    r1.place(x=100, y=180)
    r2 = Radiobutton(root, text="密码", variable=var, value='NU_code', width=5)
    r2.place(x=180, y=180)
    r3 = Radiobutton(root, text="真实姓名", variable=var, value='NU_actualname', width=5)
    r3.place(x=260, y=180)
    r4 = Radiobutton(root, text="性别", variable=var, value='NU_gender', width=5)
    r4.place(x=340, y=180)
    r5 = Radiobutton(root, text="出生日期", variable=var, value='NU_birth', width=5)
    r5.place(x=420, y=180)
    r6 = Radiobutton(root, text="电话号码", variable=var, value='NU_phonenumber', width=5)
    r6.place(x=500, y=180)

    def callback():  # 下一步button
        if var.get() == 'NU_birth':
            label = Label(root, text="新出生日期", font=("华文行楷", 15), fg="black")
            label.place(x=200, y=270)
            birth_year = StringVar()
            entry = Entry(root, textvariable=birth_year, width=10)
            entry.place(x=330, y=270)
            label = Label(root, text="年", font=("华文行楷", 15), fg="black")
            label.place(x=380, y=270)
            birth_month = StringVar()
            entry = Entry(root, textvariable=birth_month, width=10)
            entry.place(x=410, y=270)
            label = Label(root, text="月", font=("华文行楷", 15), fg="black")
            label.place(x=460, y=270)
            birth_day = StringVar()
            entry = Entry(root, textvariable=birth_day, width=10)
            entry.place(x=490, y=270)
            label = Label(root, text="日", font=("华文行楷", 15), fg="black")
            label.place(x=540, y=270)

            def callback():
                new_birth = birth_year.get() + '-' + birth_month.get() + '-' + birth_day.get()
                cur.execute("update normaluser set nu_birth = %s where nu_name = %s", [new_birth, username])
                label = Label(root, text="修改成功！", font=("华文行楷", 15), fg="black")
                label.place(x=280, y=350)

            button = Button(root, text='修改', height=1, width=20, command=callback)
            button.place(x=270, y=310)
        else:
            label = Label(root, text="新个人信息内容", font=("华文行楷", 15), fg="black")
            label.place(x=180, y=270)
            new_info = StringVar()
            entry = Entry(root, textvariable=new_info, width=20)
            entry.place(x=340, y=270)

            def callback():
                if var.get() == 'NU_name':
                    cur.execute("update normaluser set nu_name = %s where nu_name = %s", [new_info.get(), username])
                elif var.get() == 'NU_code':
                    code = new_info.get()
                    code_md5 = hashlib.md5(code.encode(encoding='utf-8')).hexdigest()  # 对输入密码进行MD5加密
                    cur.execute("update normaluser set nu_code = %s where nu_name = %s", [code_md5, username])
                elif var.get() == 'NU_actualname':
                    cur.execute("update normaluser set nu_actualname = %s where nu_name = %s",
                                [new_info.get(), username])
                elif var.get() == 'NU_gender':
                    cur.execute("update normaluser set nu_gender = %s where nu_name = %s", [new_info.get(), username])
                else:  # var.get() == 'NU_phonenumber'
                    cur.execute("update normaluser set nu_phonenumber = %s where nu_name = %s",
                                [new_info.get(), username])
                label = Label(root, text="修改成功！", font=("华文行楷", 15), fg="black")
                label.place(x=280, y=350)

            button = Button(root, text='修改', height=1, width=20, command=callback)
            button.place(x=270, y=310)

    button = Button(root, text='下一步', height=1, width=20, command=callback)
    button.place(x=270, y=220)
    root.mainloop()


# 普通用户个人信息管理页面
def NUself_admin(cur, username):
    root = Tk()
    root.title('普通用户个人信息管理')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="普通用户个人信息管理", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回', height=1, width=20, command=lambda: [root.destroy(), normal_login_successful(username)])
    button.place(x=500, y=450)

    def callback():  # 普通用户信息查询
        cur.execute("select * from NormalUser where nu_name = %s", [username])
        info_tuple = cur.fetchall()
        list_name = "用户编号   用户名         密码          真实姓名  性别  出生日期   电话号码  "
        label = Label(root, text=list_name, font=("华文行楷", 12), fg="black", bg="white")
        label.place(x=45, y=240)
        info_list = []
        for i in info_tuple:
            info_list.append(i[0])  # NU_id
            info_list.append(i[1])  # NU_name
            info_list.append(i[2])  # NU_code
            info_list.append(i[3])  # NU_actualname
            info_list.append(i[4])  # NU_gender
            info_list.append(str(i[5]))  # NU_birth
            info_list.append(i[6])  # NU_phonenumber
        info_result = " ".join(str(j) for j in info_list)
        label = Label(root, text=info_result, font=("华文行楷", 10), fg="black", bg="white")
        label.place(x=45, y=260)
    button = Button(root, text='普通用户信息查询', height=1, width=20, command=callback)
    button.place(x=150, y=110)

    def callback():
        root.destroy()
        NUself_update(cur, username)  # 普通用户个人信息修改页面
    button = Button(root, text='普通用户个人信息修改', height=1, width=20, command=callback)
    button.place(x=350, y=110)
    root.mainloop()


# 普通用户登陆成功页面
def normal_login_successful(username):
    root = Tk()
    root.title('图书销售管理系统')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="欢迎进入图书销售管理系统", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回登录', height=1, width=20, command=lambda: [root.destroy(), Login()])
    button.place(x=500, y=450)

    def callback():
        root.destroy()
        NUself_admin(cur, username)  # 用户个人信息管理页面
    button = Button(root, text='用户个人信息管理', height=1, width=20, command=callback)
    button.place(x=140, y=150)

    def callback():
        root.destroy()
        stock_admin(cur, username)  # 库存书籍管理页面
    button = Button(root, text='库存书籍管理', height=1, width=20, command=callback)
    button.place(x=350, y=150)

    def callback():
        root.destroy()
        book_purchase_admin(cur, username)  # 书籍进货管理页面
    button = Button(root, text='书籍进货管理', height=1, width=20, command=callback)
    button.place(x=350, y=200)

    def callback():
        root.destroy()
        bill_admin(cur, username)  # 财务账户管理页面
    button = Button(root, text='财务账户管理', height=1, width=20, command=callback)
    button.place(x=350, y=250)
    root.mainloop()


# 超级用户登录成功页面
def super_login_successful(username):
    root = Tk()
    root.title('图书销售管理系统')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="欢迎进入图书销售管理系统", font=("华文行楷", 20), fg="black")
    label.pack()
    button = Button(root, text='返回登录', height=1, width=20, command=lambda: [root.destroy(), Login()])
    button.place(x=500, y=450)

    def callback():
        root.destroy()
        user_admin(cur, username)  # 用户信息管理页面
    button = Button(root, text='用户信息管理', height=1, width=20, command=callback)
    button.place(x=140, y=150)

    def callback():
        root.destroy()
        stock_admin(cur, username)  # 库存书籍管理页面
    button = Button(root, text='库存书籍管理', height=1, width=20, command=callback)
    button.place(x=350, y=150)

    def callback():
        root.destroy()
        book_purchase_admin(cur, username)  # 书籍进货管理页面
    button = Button(root, text='书籍进货管理', height=1, width=20, command=callback)
    button.place(x=350, y=200)

    def callback():
        root.destroy()
        bill_admin(cur, username)  # 财务账户管理页面
    button = Button(root, text='财务账户管理', height=1, width=20, command=callback)
    button.place(x=350, y=250)
    root.mainloop()


# 登陆失败页面
def login_failed():
    root = Tk()
    root.title('图书销售管理系统')
    root.geometry("300x200+550+300")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="登录失败", font=("华文行楷", 15), fg="black")
    label.place(x=98, y=80)
    root.mainloop()


# 用户登录界面设计
def Login():
    root = Tk()
    root.title('图书销售管理系统登录')
    root.geometry("700x500+380+180")  # 宽*高+水平偏移量+竖直偏移量
    label = Label(root, text="图书销售管理系统登录", font=("华文行楷", 20), fg="black")
    label.pack()
    label = Label(root, text="用户名", font=("华文行楷", 20), fg="black",anchor="w")
    label.place(x=120, y=160)
    label = Label(root, text="密码", font=("华文行楷", 20), fg="black",anchor="w")
    label.place(x=130, y=200)

    username_in = StringVar()
    entry = Entry(root, textvariable=username_in, width=40)
    entry.place(x=220, y=160)
    code_in = StringVar()
    entry = Entry(root, textvariable=code_in, width=40, show="*")
    entry.place(x=220, y=210)

    def callback():
        code = code_in.get()  # StringVar并不是python内建的对象，而是属于Tkinter下的对象,需要用.get()函数取值
        username = username_in.get()
        code_md5 = hashlib.md5(code.encode(encoding='utf-8')).hexdigest()  # 对输入密码进行MD5加密
        cur.execute("SELECT SU_Name from SuperUser;")
        su_name_tuple = cur.fetchall()
        su_name = [i[0] for i in su_name_tuple]
        cur.execute("SELECT NU_Name from NormalUser;")
        nu_name_tuple = cur.fetchall()
        nu_name = [i[0] for i in nu_name_tuple]
        root.destroy()
        if username in su_name:
            cur.execute("SELECT SU_code from SuperUser where SU_Name=%s;", [username])
            su_code_tuple = cur.fetchall()
            if len(su_code_tuple) != 0:
                su_code = su_code_tuple[0]
            if su_code and code_md5 in su_code:
                super_login_successful(username)  # 超级用户登录成功页面
            else:
                login_failed()  # 登录失败页面
        elif username in nu_name:
            cur.execute("SELECT NU_code from NormalUser where NU_Name=%s;", [username])
            nu_code_tuple = cur.fetchall()
            if len(nu_code_tuple) != 0:
                nu_code = nu_code_tuple[0]
            if nu_code and code_md5 in nu_code:
                normal_login_successful(username)  # 超级用户登录成功页面
            else:
                login_failed()  # 登录失败页面
        else:
            login_failed()  # 登录失败页面
    button = Button(root, text='登录', height=1, width=8, command=callback)
    button.place(x=300, y=260)
    root.mainloop()


Login()

conn.commit()
conn.close()