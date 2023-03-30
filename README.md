# Bookstore_Management
Design and Implementation of Bookstore Management System


A bookstore needs a book management system to uniformly manage the purchase, sales, finance, and other aspects of books.

main functions:

1. 用户管理

 1）系统用户分为超级管理员用户和普通管理员用户。普通管理员用户只能对图书进货、销售等信息进行管理，只能查询和修改自己的用户信息；而超级管理员除了可以对图书进货、销售等信息进行管理，还能创建新的用户和查看所有用户的资料。
 
 2）超级管理员用户在系统完成时便已经存在（即其用户名和密码已经存在于数据库中）。而普通管理员用户的用户名和密码需要由超级管理员用户来创建。
 
 3）用户的密码不能以明文形式保存于数据库中，而必须先加密，一般采用MD5算法进行加密。
 
 4）每位用户除了用户名和密码信息外，还有真实姓名，工号，性别，年龄等基本信息。
 
 5）系统所有功能只有用户登录了才能进行操作
 
2. 库存书籍管理

系统中需要维护整个书城目前库存的所有书籍信息，包括书籍ISBN号，书籍名称，出版社，作者，零售价格，当前库存数量等。

3. 书籍查询

可以使用书籍编号、书籍ISBN号、书名、作者、出版社等方式查询库存的相关书籍。
 
4. 图书信息修改

可以修改书籍名称、作者、出版社、零售价格等信息。

5. 图书进货：

对于需要进货的书籍，如果库存中曾经有这本书的信息的话，则直接将这本书的ID列入进货清单，否则需要输入进货书籍的相关信息，包括ISBN号，书名，作者，出版社等。此外，每种书都要指定其进货价格和购买数量。对于刚列入进货清单的书籍给予未付款状态。

6. 进货付款：

查询正在进货的书籍，并给予付款，付款后书籍状态为已付款。

7. 图书退货：

对未付款的书籍可以进行退货，即将书籍状态改为已退货。

8. 添加新书：

对于已付款的书籍，当书籍到货后，可以将其添加到库存中，此时需要添加上书籍的零售价格。

9. 书籍购买：

使用标售零售价格购买书籍，这时书籍的库存数量需要相应地减少。

10. 财务管理：

当对书籍进货进行付款，或购买书籍时，系统的财务账户都要添加一条账单记录，记录下财务账户的支出或收入。

11. 查看账单

查看某段时间内财务账户的收入或支出记录
