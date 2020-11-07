<p align="center">
  <a href="https://argoapp.live/">
    <a href="https://imgur.com/J5O9d2O"><img src="https://i.imgur.com/J5O9d2O.png" title="source: imgur.com" alt="ArGo logo (light version)" width="210" /></a>
  </a>

  <h3 align="center">ArGo Flask Backend</h3>

  <p align="center">
   :rocket: Flask server which runs in the background for deploying code on Arweave
 </p>
</p>

> Important Notice: ArGo is in its Alpha stage. If you have a suggestion, idea, or find a bug, please report it! The ArGo team will not be held accountable for any funds lost.

## About Argo

ArGo is a one-click ☝️  deployment service platform on top of Arweave Permaweb. It offers a Vercel-like seamless experience for the developer to deploy web apps to Arweave Permaweb directly from the ArGo dashboard.

## Installation Instruction

- Create a virtual environemnt

```
python3 -m venv argovenv
```

- Activate virtual environment

```
source argovenv/bin/activate
```

- Clone repository & cd into repo

```
git clone https://github.com/argoapp-live/argo-be && cd argo-be
```

- Install dependencies

```
pip install -r requirements.txt
```

- Start Project

```
python3 app.py
```

Server will start at http://127.0.0.1:5000

## Docker Installation Instructions

- Fork or Clone this repository

```
git clone https://github.com/argoapp-live/argo-be.git
```

- Docker build - 

```
docker build -t argo-be .
```

- Docker run - 

```
docker run -v /var/run/docker.sock:/var/run/docker.sock -p 5000:5000 argo-be
```

## Contributing
Any contributions are very much welcomed. Feel free to fork and make a PR with any additions (or fixes)!

## Have questions?

Reach out to @rekpero#3898 on the ArGo Discord ([https://discord.gg/HTMqYAm](https://discord.gg/HTMqYAm)) or head to the #contributors-forum channel for further discussion!
