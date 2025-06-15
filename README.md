# Depitec Mediensteuerung

**Depitec Mediensteuerung** (dpt-media-control) ist ein Softwarepaket zur Steuerung von Geräten und Systemen auf Basis eines Raspberry Pi.

## How To use

### Voraussetzungen

Es wird empfohlen, einen Raspberry Pi 4 mit einem der letzten Raspberry Pi OS Lite Versionen zu verwenden. Dafür kann der [Raspberry Pi Imager](https://www.raspberrypi.com/software/) verwendet werden. Der Standard sollte `pi` sein.


### Herunterladen

Um das Projekt herunterzuladen, kann der folgende Befehl verwendet werden:

`git clone https://oauth2:<token>@github.com/depitec/dpt-media-control.git`

Der Token wird separat bereitgestellt und muss in der oben angegebenen URL anstelle von `<token>` eingesetzt werden.

### Installation

#### 1. Installieren der benötigten Pakete

Mit der Hilfe des `install-env.sh` scripts können alle benötigten Pakete installiert werden. Darunter `curl`, `git` und `uv` um das Programm zu starten. Das Script muss als root ausgeführt werden, da es Systempakete installiert. Zusätzlich wird `uv` in `usr/local/bin` installiert, `uv` ist notwendig um alle Abhängigkeiten und die korrekte Pythonversion zu installieren.

Das Script kann einfach via:

`sudo ./install-env.sh`

ausgeführt werden.

#### 2. Installieren der Python Abhängigkeiten

Um die Python Abhängigkeiten zu installieren, muss das `install-deps.sh` Script ausgeführt werden. Dieses erstellt ein virtuelles Python Environment und installiert alle benötigten Pakete.

! Das Script **muss** als normaler Benutzer ausgeführt werden und nicht als Root.

`./install-deps.sh`

#### 3. Starten des Systemd Dienstes

Damit das Programm auch nach einem Neustart wieder gestartet wird, wurde ein Systemd Dienst erstellt. Dieser nutzt das zuvor erstelle virtuelle Python Environment und muss nur gestartet werden.

`sudo systemctl start dpt-media-control.service`

Um zu prüfen ob der Dienst erfolgreich gestartet wurde, kann der Status des Dienstes überprüft werden:

`sudo systemctl status dpt-media-control.service`

Der Dienst sollte nun als `active (running)` angezeigt werden.

#### 4. Konfiguration

Die Konfiguration des Programms erfolgt über eine `config.toml` im Verzeichnis `.config/dpt-media-control` im Haupt Verzeichnis des Benutzers.

Um Änderungen an der Konfiguration zu übernehmen, muss diese geändert werden und anschließend der Dienst neugestartet werden:

`sudo systemctl restart dpt-media-control.service`

