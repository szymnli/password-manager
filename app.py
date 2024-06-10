import click, json

class Vault:
    def __init__(self, master_key, passwords = {}):
        self.master_key = master_key
        self.passwords = passwords


    def add_password(self, service, username, password):
        self.passwords[service] = {
            "Username": username,
            "Password": password
        }

    def get_password(self, service):
        return self.passwords[service]
    
    def authenticate(self, value):
        return value == self.master_key
    
    @property
    def master_key(self):
        return self._master_key
    
    @master_key.setter
    def master_key(self, value):
        self._master_key = value

    @property
    def passwords(self):
        return self._passwords
    
    @passwords.setter
    def passwords(self, value):
        self._passwords = value
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = value

def main():
    click.clear()
    master_pass = "1234"
    print("Welcome to the password manager")

    try:
        with open("vault.json") as file:
            passwords = json.load(file)
            vault = Vault(master_pass, passwords)
    except FileNotFoundError:
        vault = Vault(master_pass)

    if authenticate(vault):
        print("Authenticated")
        menu(vault)
    else:
        print("Not authenticated")

def menu(vault):
    while True:
        click.clear()
        click.echo("1. Add password")
        click.echo("2. Get password")
        click.echo("3. List services")
        click.echo("0. Exit")
        click.secho("Enter an option: ", nl=False, fg="blue")
        option = click.getchar()

        match option:
            case "1":
                add_password(vault)
            case "2":
                get_password(vault)
            case "3":
                list_services(vault)
            case "0":
                click.clear()
                break
            case _:
                click.secho("\nInvalid option", fg="red")
                click.pause()

def list_services(vault):
    click.clear()
    for i, service in enumerate(vault.passwords):
        click.echo(f"{i+1}. {service}")
    click.pause()

def add_password(vault):
    click.clear()
    service = click.prompt("Enter the service")
    username = click.prompt("Enter the username")
    password = click.prompt("Enter the password", hide_input=True)
    vault.add_password(service, username, password)
    with open("vault.json", "w") as file:
        json.dump(vault.passwords, file, indent=4)
    click.pause()

def get_password(vault):
    click.clear()
    service = click.prompt("Enter the service")
    passw = vault.get_password(service)
    click.clear()
    click.secho(f"Service: {service}", bold=True)
    click.echo(f"Username: {passw['Username']}")
    click.echo(f"Password: {passw['Password']}")
    click.pause()

def authenticate(vault):
    master_key = input("Enter the master key: ")
    return vault.authenticate(master_key)

if __name__ == '__main__':
    main()