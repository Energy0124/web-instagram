Web Instagram
==
- The website on the openshift server:
  - http://web-instagram-web-instagram-2018.a3c1.starter-us-west-1.openshiftapps.com

Developer
--
**Name:** Ling Leong

**SID:** 1155062557

**UNIX ID:** lling5

Project structure:
--
- _sample data:_
  - sample sql data for testing
- _sql:_
  - sql for creating database table
- _upload:_
  - store uploaded images
- _cgi-bin:_
  - **cgi_helper.py:** a custom python module containing useful utility functions for this website
  - **editor.py:** image filter page
  - **index.py:** index page and image listing
  - **init.py:** initialization page
  - **init_handler.py:** handling admin password initialization
  - **login.py:** display login page
  - **login_handler.py:** handling login
  - **logout_handler.py:** handling logout
  - **register.py:** display register page
  - **register_handler.py:** handling register
  - **save.py:** handle image saving and permalink display
  - **test.py:** visit counter for testing
  - **update_password.py:** display update password page
  - **update_password_handler.py:** handle update password
  - **upload.py:** handle image upload and validation
  - ***.html:** html template for the corresponding .py file
- _/:_
  - **app.py:** main web cgi server 

Project description
--
1. For this project, I first implement the Access Control & Session Management.
I use SQLite 3 as the database. Users table is created. Register, login and password update are also implemented in this stage.
2. After access control, index page and file upload are then implemented. Images table is created to store the images related records. Next, image listing in index and pagination are implemented.
3. After that, editor functions are implemented, handling filters, discarding and permalinks, etc.
4. Finally, system initialization is implemented. As well as varies, bug fixes and improvement are done.


