# ReelPick

This is a website that is designed to be used by film-clubs. The admin can post a movie and then the members can write the reviews under.

## Features

- **Film management** – Admins can add films with posters and descriptions
- **Reviews** – Logged in users can write reviews on films. All reviews are encrypted in the database.
- **Activity logging** – All important actions are logged with timestamp and IP address

## Technology

- **Backend & Frontend:** Python / Django
- **Database:** SQLite
- **Encryption:** Cryptography (Fernet)
- **Hosting:** Ubuntu Server on Proxmox
- **Version control:** Git / GitHub

## Installation & setup

1. Clone the repository:
```bash
git clone https://github.com/Benjamin-LucasM/Film-Review.git
cd Film-reviw/filmsite
```

2. Create and activate virtual enviroment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Getting your cryptation key
    - python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    - `touch .env`
    - `nano .env`
    - write "FERNET_KEY = <key>

4. Run migrations and create a super user
```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```

5. Start the server
```bash
python3 manage.py runserver <ip-address>
```

