# proxyServerForStableDiffusion

## Usage
### 1. Modify local_config.py file


### 2. Build docker image
```bash
sudo docker build --tag proxyServer .
```

### 3. Run proxyServer
```bash
sudo docker run -d --restart always -p 5000:5000 proxyServer 
```