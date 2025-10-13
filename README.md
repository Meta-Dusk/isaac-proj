# Isaac Project

This app is made for a school project.

## Installation/Setup

### Usual Installation and Setup

Go to the releases tab to the right, and download the latest version, and follow the instructions written there.

### App Caveats

Sometimes the app doesn't have write permissions, so it cannot output a text file. To fix this, just run it as `administrator` and launch the app again. This should make a directory for the output, including the output file expected there. You don't have to do this, as the output will be shown, and you can just copy it to your clipboard by clicking it.

### Setup for Developers

If you wish to run the code yourself, it'll be easy if you have `uv` as the package manager! If you don't have it, you can just simply install it with your usual `pip install` like so:

```bash
pip install uv
```

After installing, or if you already have `uv`, you can just simply clone this repo to your desired directory, or download the zip file. If you've already done that, make sure that you didn't leave the `pyproject.toml` file, as this is required for downloading the dependencies automatically. Since we'll be using `uv`, you can now just simply do these commands:

```uv
uv sync
```

That command will download all the dependencies found in the `pyproject.toml` file, however, it will exclude the dev dependencies. If you wish to build the app yourself as well, then just simply add the `--dev` flag to it, as shown below:

```uv
uv sync --dev
```

That will download everything including the optional dev dependencies. Moving on, if there's a problem with the installation, it could be because `uv` is attempting to download prerelease versions of the dependencies. To fix this, simply add a different flag; `--prerelease=allow`, like so:

```uv
uv sync --prerelease=allow
```

That should download the prerelease versions that I used for this project. After doing all that, you can also do:

```uv
uv lock
```

Just to be sure. What that does, is simply lock the versions of the dependencies that are downloaded, so that they do not get changed suddenly, like if `flet` decided to download other dependencies for some reason, which could happen. After doing all that, you're all set! `uv` will start a virtual environment automatically for you, so you can just test the `flet` app if it works, by doing this:

```uv
uv run flet run
```

Running commands are the same like before without `uv`, but since we're using `uv`, you can _optionally_ add the `uv run` prefix. This won't do much, but it's best to use that prefix just in case. That's it! It's up to you what you're going to do with the code, I already included a good amount of documentation inside the code (docstrings), and there are also tools for helping with building the app. The tools are found in the `./tools/` directory, which can be found in the root directory. Just refer to the comments I added there if you wish to use them. Building the app is also easy, and this app is meant for windows, so I only tested it for windows. The command you'd do if you're going to build it manually, is this:

```uv
uv run flet build windows -v
```

That will start building the app, and download everything that it needs. Since you'll be running that first time, it'll take a while, since it'll download `Flutter` if you don't already have it installed. You can also just run the `build_app.py` script, and it will build the app, and even the installer. BUT, if you do not have a `signtool`, this will NOT work. So, you can just don't do the installer then, by adding the `--no-installer` flag when running the build script. You can also add a `--help` or `-h` so you can see the available flags to use, when running the build app script. That's all!

## Feature List

| Feature | Description |
| ----- | ----- |
| **Data Encryption** | Any input will be encrypted with a click of a button. |
| **Data Decryption** | Any input that can be decrypted, will be decrypted with a click of a button. |
| **Optional Output** | The output will be displayed, and you can also let it output to a text file in a set directory. |
| **Copy to Clipboard** | You can click the output to copy it directly into your clipboard. |

## Known Issues and Solutions

| No. | Issue | Description | Solution | Severity |
| -------- | -------- | -------- | -------- | -------- |
| 1. | Stuck on Loading Screen. | This could be because your device is struggling to run the app. | Simply close then open the executable again. | Easily fixed. |
