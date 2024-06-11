import click, json, clipboard, cryptmoji, random, string


class Vault:
    def __init__(self, master_key, passwords={}):
        self.master_key = master_key
        self.passwords = passwords

    def add_password(self, service, username, password):
        self.passwords[service] = {"Username": username, "Password": password}

    def get_password(self, service):
        return self.passwords[service]

    def delete_password(self, service):
        del self.passwords[service]

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
    auth = False
    while not auth:
        click.clear()
        vault = start()
        if authenticate(vault):
            click.secho("Authentication successful", fg="green")
            click.pause()
            menu(vault)
            auth = True
        else:
            click.secho("Invalid master key", fg="red")
            click.pause(info="Press any key to try again...")


def start():
    click.clear()
    click.secho("Welcome to the password manager", fg="magenta")

    try:
        with open(".master.json") as file:
            master_pass = json.load(file)
    except FileNotFoundError:
        vault, master_pass = first_time()

    try:
        with open(".vault.json") as file:
            passwords = json.load(file)
            vault = Vault(master_pass, passwords)
    except FileNotFoundError:
        with open(".vault.json", "w") as file:
            json.dump({}, file)

    return vault


def first_time():
    click.secho(
        "Choose a strong password and remember not to share it with anyone!\n",
        fg="yellow",
        italic=True,
    )
    master_pass: str = click.prompt(
        "Create your master password", hide_input=True, confirmation_prompt=True
    )
    click.clear()
    with open(".master.json", "w") as file:
        master_pass = cryptmoji.encrypt(master_pass)
        json.dump(master_pass, file)
    return Vault(master_pass), master_pass


def menu(vault):
    while True:
        click.clear()
        click.secho("Main Menu", fg="magenta")
        click.echo("1. Add password")
        click.echo("2. Get password")
        click.echo("3. List services")
        click.secho("0. Exit", fg="blue")
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


def service_menu(vault, service):
    while True:
        click.clear()
        click.secho(service, fg="magenta")
        click.secho(f"Username: {vault.passwords[service]["Username"]}", fg="magenta")
        click.echo("1. Show password")
        click.echo("2. Copy to clipboard")
        click.echo("3. Edit entry")
        click.echo("4. Delete entry")
        click.secho("0. Go back", fg="blue")
        click.secho("Enter an option: ", nl=False, fg="blue")
        option = click.getchar()

        match option:
            case "1":
                click.secho(
                    f"\nPassword: {cryptmoji.decrypt(vault.passwords[service]['Password'], key=vault.master_key)}",
                    fg="yellow",
                )
                click.pause()
            case "2":
                clipboard.copy(
                    cryptmoji.decrypt(
                        vault.passwords[service]["Password"], key=vault.master_key
                    )
                )
                click.secho("\nPassword copied to clipboard!", fg="yellow")
                click.pause()
            case "3":
                add_password(vault, service)
            case "4":
                click.clear()
                click.secho(
                    f"Are you sure you want to delete password for {service}?", fg="red"
                )
                click.echo("1. Yes")
                click.echo("2. No")
                while True:
                    match click.getchar():
                        case "1":
                            vault.delete_password(service)
                            with open(".vault.json", "w") as file:
                                json.dump(vault.passwords, file, indent=4)
                            click.secho("Password deleted successfully", fg="green")
                            click.pause()
                            return
                        case "2":
                            break
                        case _:
                            click.secho("Invalid option", fg="red")

            case "0":
                click.clear()
                return
            case _:
                click.secho("\nInvalid option", fg="red")
                click.pause()


def list_services(vault):
    click.clear()
    click.secho("Services", fg="magenta")
    if not vault.passwords:
        click.secho("No services found", fg="red")
        click.pause()
        return
    for i, service in enumerate(vault.passwords):
        click.echo(f"{i+1}. {service}")

    click.secho("0. Go back", fg="blue")
    choice = click.prompt(
        click.style(
            f"Choose a service to view details [1-{len(vault.passwords)}]", fg="blue"
        ),
        type=click.IntRange(0, len(vault.passwords)),
    )

    if choice != 0:
        service = list(vault.passwords.keys())[choice - 1]
        service_menu(vault, service)
    else:
        return


def add_password(vault, _service=None):
    click.clear()
    if _service:
        click.secho(f"Edit {_service}", fg="magenta")
        service = _service
    else:
        click.secho("Add password", fg="magenta")
        service = click.prompt("Enter the service")
        if service in vault.passwords:
            click.secho("Service already exists", fg="red")
            click.pause()
            return
    username = click.prompt("Enter the username")
    click.echo("1. Enter the password")
    click.echo("2. Generate a strong password")
    while True:
        match click.getchar():
            case "1":
                password = click.prompt(
                    "Enter the password", hide_input=True, confirmation_prompt=True
                )
                break
            case "2":
                length = click.prompt(
                    "Enter the length of the password",
                    type=click.IntRange(8, 32),
                    default="8-32",
                    show_default=True,
                )
                password = password_generator(vault, length)
                click.secho(
                    f"Generated password: {password}", fg="green"
                )  # TODO: Implement password generator
                clipboard.copy(cryptmoji.decrypt(password, key=vault.master_key))
                click.secho("Password copied to clipboard", fg="yellow")
                break
            case _:
                click.secho("Invalid option", fg="red")

    password = cryptmoji.encrypt(password, key=vault.master_key)
    vault.add_password(service, username, password)
    with open(".vault.json", "w") as file:
        json.dump(vault.passwords, file, indent=4)
    click.pause(
        info=f"\n{click.style('Password added successfully!', fg="green")} \nPress any key to continue..."
    )


def get_password(vault):
    click.clear()
    click.secho("Get password", fg="magenta")
    if vault.passwords:
        while True:
            click.secho("Enter 0 to go back", fg="blue")
            service = click.prompt("Enter the service")
            if service == "0":
                break
            elif service not in vault.passwords:
                click.secho("Service not found", fg="red")
            else:
                break
        if service == "0":
            return
        passw = vault.get_password(service)
        while True:
            click.clear()
            click.secho(service, fg="magenta")
            click.echo(f"Username: {passw['Username']}")
            click.echo(f"Password: {passw['Password']}")
            click.echo("1. Copy to clipboard")
            click.echo("2. Show password")
            click.secho("0. Go back", fg="blue")
            match click.getchar():
                case "1":
                    clipboard.copy(
                        cryptmoji.decrypt(passw["Password"], key=vault.master_key)
                    )
                    click.secho("Password copied to clipboard", fg="yellow")
                    click.pause()
                case "2":
                    click.secho(
                        f"Password: {cryptmoji.decrypt(passw['Password'], key=vault.master_key)}",
                        fg="yellow",
                    )
                    click.pause()
                case "0":
                    break
                case _:
                    click.secho("Invalid option", fg="red")
                    click.pause()

    else:
        click.secho("No services found", fg="red")
        click.pause()
        return


def authenticate(vault):
    master_key = click.prompt("Enter your master key", hide_input=True)
    master_key = cryptmoji.encrypt(master_key)
    return vault.authenticate(master_key)


def password_generator(vault, length: int):
    password = "".join(random.choice(string.printable) for _ in range(length))
    return cryptmoji.encrypt(password, key=vault.master_key)


if __name__ == "__main__":
    main()
