# password-manager
### Description:
This is a simple CLI password manager, that uses `cryptmoji` to encrypt and decrypt your passwords using cool emojis! All your password are encrypted and stored locally in the `.vault.json` file, to access them you need to use your own master key that's also encrypted and stored, this time in `.master.json`.

With this password manager you can easilly store, access, list, edit, delete and generate passwords for all your favorite services!

#### Vault class
Vault class is the core of the whole project, it's responsible for creating the vault itself, given a master key; adding, fetching and deleting passwords, and also for authenticating the user before giving access to all the passwords.
This class is equiped with getters and setters for the master key, username and password entries.

#### Main function
Main function is responsible for calling the `start` function and then `authenticate` and based on the return value, giving or denying access to the vault.

#### Start function
This is the first function called by the program, it greets the user and checks for `.vault.json` and `.master.json` files' existance, based on that either creates a vault from these files or calls the `first_time` function to set up a brand new vault.
Return value is a vault object.

#### First_time function
Here user is being prompted for a master key to set up the vault with. Once the user confirms their password `.master.json` file gets created and an encrypted version of the master key is added to it.
Return value is a tuple containing a vault object and the encrypted password.

#### Authenticate function
This function prompts user for the master key, encrypts it and compares with the one associated with the vault. Function returns a boolean value based on the comparasing.

#### Menu function
This function contains a while loop with all of the main options available, these options are enumerated and displayed one by one and the user is able to choose one based on a single character input, managed by a switch. Options are as follows:
```
1. Add password
2. Get password
3. List services
0. Exit
```
Each one of them calls their respective function, excluding `0.` which just breaks out of the loop, effectively exiting the program.

#### Add password function
This function is used for both adding and editing existing entires, it  takes either one or two arguments, the `vault` object and optionally `_service` with a default value of `None`.

If there is no service provided user is prompted for the service's name, username and a choice for either creating the password themselves or generating one; if the user chooses to create one they get prompted for it with an additional confirmation prompt and it gets encrypted and saved to both the vault and the `.vault.json` file, and if user chooses to generate one, they get prompted for a password length and a separate `password_generator` function creates and returns a strong encrypted password, that gets copied to user's clipboard automatically and is also displayed in an enrcypted/emojified way.

And if the function is called with a `_service` argument the function no longer prompts the user for the service's name and continues to function the same way as with adding a new one.
```
Add password
Enter the service: CS50
Enter the username: student@cs50
1. Enter the password
2. Generate a strong password
Enter the length of the password [8-32]: 17
Generated password: 🧟❔🆓🈲🩸🆙🈺🩹🧾🪓✅🧢🧹🧞🈁🈵➖
Password copied to clipboard

Password added successfully!
Press any key to continue...
```

#### Password generator function
This function creates a string of specified length with random "printable" letters, this is possible thanks to the `random` and `string` modules. After the password is generated, an encrypted version of it is returned.

#### Get password function
Firstly this function checks if the vault is not empty, if it is "No services found" message is being displayed and the user can go back to the main menu, but if the vault is not empty user is prompted for a name of the service they wish to access, after successfully providing the service, username and encrypted password are displayed, along with options to either copy to clipboard, show the decrypted version of the password or go back.
```
Get password
Enter 0 to go back
Enter the service:
```
```
Google
Username: user@gmail.com
Password: 🆙🈁🆚🆕🆕🃏🆖❔🈁🆙
1. Copy to clipboard
2. Show password
0. Go back
```

#### List services function
This one provides the user with an enumerated list of all services saved to the vault, and a prompt for corresponding numeric value next to the service's name, if a valid option is provided the user is being redirected to the `service_menu' of the chosen service.
```
Services
1. Google
2. Facebook
3. GitHub
4. Twitter
5. Usos
6. CS50
0. Go back
Choose a service to view details [1-5]:
```
#### Service menu function
Once accessed user is shown a list of previously mentioned available actions and a prompt to choose any of them.
```
CS50
Username: student@cs50
1. Show password
2. Copy to clipboard
3. Edit entry
4. Delete entry
0. Go back
Enter an option:
```

#### UI/UX
Library called `click` was chosen to create the CLI, because of the ease of use and amount of functionality it provides.

#### Encryption
For encryption and decryption the previously mentioned library `cryptmoji` was used. It was chosen because it seemed like a fun spin on encryption that is rarely used.

#### Storing the vault
The vaults are stored locally and not, for example in a cloud based database, due to this being a small project and there not being any plans for future scaling or publishing
