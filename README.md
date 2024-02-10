# contactus - your personal crm
#### Video Demo: https://youtu.be/t4FinUemou4 
#### Description:

### Objective
I wished to have one place to store basic information, notes (for example for gift ideas) and – **this is the most important feature** – the date of last contact with friends and acquaintances.
> *"... phew, you really haven't seen your programming buddy for two months?!"* 🫢

### Approach
First, the web-app needs a database to store the user's input long-term. This is solved via SQLite and the cs50 library with which two tables are created: One for users and user authentification, another for all the contacts and contact information of each user.

Second, the stored data is sensitive and maybe others want to use contactus too. The web-app therefore needs some user authentification. This is solved via registration/login and individual user ids plus their belonging user sessions after succesful login.

The web-app needs a homepage showing a list of all the user's contacts plus also the possibility to add further contacts, edit existing contacts, search through stored contacts and – supporting the most important feature – **edit a date (last seen/contact) by only hitting one button:**
> *"... yep, you're good – you've seen this one today."* 🫡

Also it is nice to be able to adjust some basic settings: changing password and username or – bravely stepping into danger zone 💀 – delete all contacts or the account and make use of the **_right to erasure of personal data_**.

> *"... choose wisely – your friends be gone and there's no way back."* 🫣

### Details
#### layout.html
The layout operates as the skeleton of the web-app, as it contains constant components such as head, nav and footer as well as replaceable parts that are served by the content of the other files: the page's title, the nav's content depending on a user being logged in or not, potential flashed messages and the page's main content.

#### register.html
This page contains a form to choose a username and a password that has to be typed in twice. If the username already exists, there'll pop up a flash message. The same happens when the second password doesn't confirm the first password.

#### login.html
This page is loaded as first if a user is not registrated yet or logged in. It contains a form to type in the correct username and password. If the username does not exist or the password is not associated with the username or does not exist, flash messages will pop up in each case.

#### index.html
The index is the starting page and loaded as first when a user just registrated or logged in. It contains a list of all user's contacts, if any, and offers the possibilty to add further contacts, edit existing contacts, search through stored contacts and edit a contact's date (last seen/contact). If there are no contacts stored yet, it only offers the possibility to add a contact.

#### add-contact.html and edit-contact.html
Both pages serve as skeleton for form.html. They differ in edit-contact.html receiving information via URL (contact id) to prefill the form with the corresponding contact data and also not just submitting edited contact data but also the corresponding contact id back via a hidden input field.

#### form.html
This contains the form which is rendered in add-contact.html and edit-contact.html. It is asking for user input to store a contact's basic information, notes and date of last contact including email verification.

#### settings.html
The settings page contains input fields to change the password or username as well as the options to delete all contact data or the account. The input for the password checks for the old password being the correct one. If not, there will be a flash message popping up. The field for the username checks if the old username is the right one and if the new username is not already existing.

#### styles.css
... only containing some css adjustments to bootstrap's framework to make the web-app look like ... it looks. 💁🏼
















